import pandas as pd
from bs4 import BeautifulSoup
import datetime
import smtplib
import ssl
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import concurrent.futures
import random
import time

# 发送主函数
def send_mail(sender, sender_alias, sender_pwd, recipient_list, subject, body, host="smtp.qcloudmail.com", port=465, is_use_ssl=True):
  try:
      message = MIMEMultipart('alternative')
      message['Subject'] = Header(subject, 'UTF-8')
      message['From'] = formataddr([sender_alias, sender])
      message['To'] = ",".join(recipient_list)
      to_addr_list = recipient_list

      mime_text = MIMEText(body, _subtype='html', _charset='UTF-8')
      message.attach(mime_text)

      if is_use_ssl:
          context = ssl.create_default_context()
          context.set_ciphers('DEFAULT')
          client = smtplib.SMTP_SSL(host, port, context=context)
      else:
          client = smtplib.SMTP(host, port)
      client.login(sender, sender_pwd)
      client.sendmail(sender, to_addr_list, message.as_string())
      client.quit()

      return 'Send email success!'
  except smtplib.SMTPException as e:
      return f"SMTP error: {e}"
  except Exception as e:
      return f"Other error: {e}"

def single_send(sender, sender_alias, sender_pwd, playerInfoDict, soup):
    for k, v in playerInfoDict.items():
        if soup.find(id=k):
            soup.find(id=k).string = v
    recipient_list = [playerInfoDict['emailAddress']]
    subject = playerInfoDict['subject']
    body = soup.prettify()
    smtp_host = "smtp.qcloudmail.com"
    smtp_port = 465
    is_using_ssl = True
    single_result = send_mail(sender, sender_alias, sender_pwd, recipient_list, subject, body, smtp_host, smtp_port, is_using_ssl)
    return single_result


# 读取配置文件
df = pd.read_json(r'sender.json')
sender = df['username'][0]
sender_alias = 'WinTokens'
sender_pwd = df['password'][0]

print(sender, sender_alias, sender_pwd)

# 指定发送任务和模板
sendMission = 'temple/task.csv'
sendTemple = 'temple/test.html'

df_sendTask = pd.read_csv(sendMission)
sendDict = df_sendTask.to_dict(orient='records')
soup = BeautifulSoup(open(sendTemple), 'html.parser')
multi_result = []

def single_send_with_sleep(sender, sender_alias, sender_pwd, playerInfoDict, soup):
    # 随机睡眠 0-5 秒
    time.sleep(random.uniform(0, 5))
    # 调用原始的 single_send 函数
    single_result = single_send(sender, sender_alias, sender_pwd, playerInfoDict, soup)
    playerInfoDict['result'] = single_result
    return playerInfoDict

multi_result = []

with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(single_send_with_sleep, sender, sender_alias, sender_pwd, playerInfoDict, soup) for playerInfoDict in sendDict]
    for future in concurrent.futures.as_completed(futures):
        try:
            result = future.result()
            multi_result.append(result)
        except Exception as e:
            print(f"线程执行出错: {e}")



df_result = pd.DataFrame(multi_result)
df_result.to_csv('excel/result.csv', index=False)