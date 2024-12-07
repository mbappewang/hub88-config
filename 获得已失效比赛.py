import pandas as pd
import requests
from datetime import datetime
import hub88_api as hub88

# 读取配置文件
df = pd.read_json(r'pwd.json')
clientId = df['clientId'][0]
password = df['password'][0]

print(clientId, password)

# 获取初始 token
token = hub88.get_token(clientId, password)

def get_sports():
    url = f'https://bet-hub88.prod.wintokens.io/hub88/sportsData'
    response = requests.get(url)
    
    # 检查响应状态码
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return None
    
    # 检查响应内容
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("响应内容不是有效的 JSON 格式")
        print("响应内容:", response.text)
        return None

def get_leagues(sportId, type, hours):
    url = f'https://bet-hub88.prod.wintokens.io/hub88/league?sportId={sportId}&type={type}&hours={hours}'
    response = requests.get(url)
    
    # 检查响应状态码
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return None
    
    # 检查响应内容
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("响应内容不是有效的 JSON 格式")
        print("响应内容:", response.text)
        return None
    
def get_events(sportId, type, hours, leagueId):
    url = f'https://bet-hub88.prod.wintokens.io/hub88/league/matches?sportId={sportId}&type={type}&hours={hours}&leagueId={leagueId}'
    response = requests.get(url)
  
    # 检查响应状态码
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return None
    
    # 检查响应内容
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("响应内容不是有效的 JSON 格式")
        print("响应内容:", response.text)
        return None
    
def get_eventInfo(eventId):
    url = f'https://bet-hub88.prod.wintokens.io/hub88/matchInfo?eventId={eventId}'
    response = requests.get(url)
  
    # 检查响应状态码
    if response.status_code != 200:
        print(f"请求失败，状态码: {response.status_code}")
        return None
    
    # 检查响应内容
    try:
        return response.json()
    except requests.exceptions.JSONDecodeError:
        print("响应内容不是有效的 JSON 格式")
        print("响应内容:", response.text)
        return None

sport_response = get_sports()
sport_data = sport_response.get('data', None)
sportIds = []
for i in sport_data:
    if i['count']['live'] != 0:
        sportIds.append(i['sportId'])
print(sportIds)

events_list = []
s = 0
for i in sportIds:
  s += 1
  league_response = get_leagues(i, 0, 0)
  league_data = league_response.get('data', None)
  league_list = []
  if league_data is not None:
    for j in league_data:
        if league_data is not None:
          league_list.append(j['leagueId'])
  # print(league_list)

  k=0
  for j in league_list:
    events_response = get_events(i, 0, 0, j)
    events_data = events_response.get('data', None)
    # print(events_data)
    if events_data is not None:
      events_list.extend(events_data)
    k += 1
    print(f"运动进度{s}/{len(sportIds)} / 联赛进度{k}/{len(league_list)}")

eventIds = []
for i in events_list:
    eventIds.append(i['eventId'])


event_result_list = []
j = 0
sport_dict = {}
for sport in sportIds:
    sportName_trans = hub88.get_all_translation(token, sport, "sport")
    sportName = sportName_trans['translations']['en']
    sport_dict[sport] = sportName
for i in eventIds:
    eventInfo = get_eventInfo(i)
    eventData = eventInfo.get('data', None)
    if events_data is not None:
        event_item = {}
        event_item['sportId'] = eventData['sportId']
        event_item['sportName'] = sport_dict[eventData['sportId']]
        event_item['locationName'] = eventData['locationName']
        event_item['leagueName'] = eventData['leagueName']
        event_item['eventName'] = eventData['eventName']
        event_item['eventId'] = eventData['eventId']
        if eventData['markets'] is not None:
            event_item['全部market个数'] = len(eventData['markets'])
            lenmkt = 0
            for mkt in eventData['markets']:
                if mkt['tradingStatus'] == 0:
                    lenmkt += 1
            event_item['可交易market个数'] = lenmkt
        else:
            event_item['全部market个数'] = 0
            event_item['可交易market个数'] = 0


        event_item['status'] = eventData['status']
        event_item['tradingStatus'] = eventData['tradingStatus']
        # 将 Unix 时间戳转换为本地时间类型
        start_time = datetime.fromtimestamp(eventData['startTime'])
        event_item['startTime'] = start_time.strftime('%Y-%m-%d %H:%M')
        # 计算距离现在的时间差
        time_diff = datetime.now() - start_time
        days, seconds = time_diff.days, time_diff.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        event_item['timeDiff'] = f"{days}天 {hours}小时 {minutes}分钟 {seconds}秒"
        print(event_item['timeDiff'])
        event_result_list.append(event_item)
    j += 1
    print(f"比赛进度{j}/{len(eventIds)}")

df = pd.DataFrame(event_result_list)
df_filtered = df[(df['status'] == 3)]
df_filtered.to_excel('excel/已失效比赛.xlsx', index=False)