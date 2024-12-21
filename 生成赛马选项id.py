import pandas as pd
import requests

def get_eventData(eventId):
  url = f'https://bet-hub88.prod.wintokens.io/hub88/thoroughbred/detail?eventId={eventId}'
  headers = {
    'Accept-Language':'ja'
  }
  response = requests.get(url,headers=headers)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print(f"获取失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code
  
def get_selectionId(data,marketId,finishPoslist):
  targetHorseList = []
  selections = []
  # 遍历比赛结果，获取指定名次的马信息
  for horse in data['race']['competitors']:
    horseInfo = {}
    if horse['finishPosition'] in finishPoslist:
      horseInfo['eventId'] = data['eventId']
      horseInfo['eventName'] = data['locationName'] + ' -- ' + data['name']
      horseInfo['horseNmae'] = horse['name']
      horseInfo['programNumber'] = horse['programNumber']
      horseInfo['finishPosition'] = horse['finishPosition']
      targetHorseList.append(horseInfo)
  # 遍历market获取指定market的选项信息
  for market in data['race']['market']:
    if market['id'] == marketId:
      selections = market['selections']
      break
  # 遍历选项信息，找出目标选项
  for horse in targetHorseList:
    horse['selectionId'] = selections[int(horse['programNumber'])-1]['id']
    horse['horseNameTrans'] = selections[int(horse['programNumber'])-1]['name']
    horse['marketId'] = marketId
  return targetHorseList

eventIds = [6809030,6809032,6808980,6808981]
# 12314435 -> 单胜 ; 12322021 -> 复胜 ; 
marketId = 12314435
finishPoslist = [2]
resultlist = []
for event in eventIds:
  repsonse = get_eventData(event)
  data = repsonse.get('data',None)
  if data is not None:
    resultlist = resultlist + get_selectionId(data,marketId,finishPoslist)

df = pd.DataFrame(resultlist)
df.to_excel(f'excel/赛马2-5名.xlsx',index=False)