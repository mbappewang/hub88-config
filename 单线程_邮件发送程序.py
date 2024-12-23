import pandas as pd
from bs4 import BeautifulSoup
import datetime
import smtplib
import ssl
from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

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
            soup.find(id=k).string = str(v)
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
# sendMission = 'temple/thanks.csv'
# sendTemple = 'temple/thanks.html'

df_sendTask = pd.read_csv(sendMission)
sendDict = df_sendTask.to_dict(orient='records')
soup = BeautifulSoup(open(sendTemple), 'html.parser')
multi_result = []

for playerInfoDict in sendDict:
    single_result = single_send(sender,sender_alias,sender_pwd,playerInfoDict, soup)
    playerInfoDict['result'] = single_result
    print(playerInfoDict)
    multi_result.append(playerInfoDict)
    df_result = pd.DataFrame(multi_result)
    df_result.to_csv('excel/1222result.csv', index=False)