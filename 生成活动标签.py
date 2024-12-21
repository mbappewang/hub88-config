import pandas as pd
import requests
import yaml

def get_eventData():
  url = f'https://bet-hub88.prod.wintokens.io/hub88/thoroughbred?sportId=457&type=2'
  headers = {
    'Accept-Language':'en'
  }
  response = requests.get(url,headers=headers)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print(f"获取失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code
  
results_data = get_eventData()
data = results_data.get('data',None)
tagList = []
secondRefundEventIds = [6808980,6808981,6809030,6809032]
if data is not None:
  for leagues in data:
    if leagues['locationId'] == 59:
      for race in leagues['race']:
        for match in race['matches']:
          tag = {}
          tag['eventId'] = match['eventId']
          if match['eventId'] in secondRefundEventIds:
            tag['marketId'] = 12314435
            tag['tag'] = "単勝 2nd Refund"
            tagList.append(tag)
        for match in race['matches']:
          tag = {}
          tag['eventId'] = match['eventId']
          tag['marketId'] = 20714345
          tag['tag'] = f"馬連馬単3連単 10% LoseBack"
          tagList.append(tag)
df = pd.DataFrame(tagList)

# 保存为yaml
save_path = r'yaml/hub88_activity_tag.yaml'
with open(save_path, 'w', encoding='utf-8') as f:
    yaml.dump(df.to_dict(orient='records'), f, 
    allow_unicode=True,  # 支持中文
    default_flow_style=False,  # 使用块状格式
    sort_keys=False,  # 不对键进行排序
    indent=2)  # 设置缩进为2个字符