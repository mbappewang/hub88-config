import pandas as pd
import requests

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
eventIds = []
if data is not None:
  for leagues in data:
    if leagues['locationId'] == 59:
      for race in leagues['race']:
        for match in race['matches']:
          eventIds.append(match['eventId'])
df = pd.DataFrame(eventIds)
df.to_excel(f'excel/eventIds.xlsx',index=False)