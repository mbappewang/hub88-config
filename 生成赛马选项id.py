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

eventIds = [6748309, 6746471, 6746467, 6746475, 6746490, 6746496, 6746493, 6746479, 6746494, 6746486, 6746502, 6746492, 6746441, 6746443, 6746445, 6746448, 6746455, 6746450, 6746483, 6746460, 6746468, 6746463, 6746472, 6746478, 6746451, 6746458, 6746466, 6746454, 6746462, 6746473, 6746476, 6746480, 6746484, 6746491, 6746487, 6746435, 6746437, 6746439, 6746440, 6746442, 6746444, 6746449, 6746456, 6746447, 6746452, 6746464, 6746459]
# 12314435 -> 单胜 ; 12322021 -> 复胜 ; 
marketId = 12314435
finishPoslist = [2,3,4,5]
resultlist = []
for event in eventIds:
  repsonse = get_eventData(event)
  data = repsonse.get('data',None)
  if data is not None:
    resultlist = resultlist + get_selectionId(data,marketId,finishPoslist)

df = pd.DataFrame(resultlist)
df.to_excel(f'excel/赛马2-5名.xlsx',index=False)