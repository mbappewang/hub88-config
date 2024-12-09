import requests
import pandas as pd

def getList(current,languageType,orderBy,sportId,type):
  url = f'https://sportapi.fastball2.com/v1/match/getList'
  payload = {
    "current" : current,
    "isPC" : True,
    "languageType" : languageType,
    "orderBy" : orderBy,
    "sportId" : sportId,
    "type" : type
  }
  response = requests.post(url,json=payload)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print(f"获取schedule失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code
 
# 映射关系
df = pd.read_csv('excel/映射表.CSV')
df['FB_id'] = df['FB_id'].astype(str)
df['home_team_id'] = df['home_team_id'].astype(str)
mapping = df.set_index('FB_id')['home_team_id'].to_dict()


getResult = getList(1,"ENG",1,1,4)
data = getResult.get('data',None)
if data is not None:
  matches = data.get('records',None)

pageLength = data.get('pageTotal',None)
matchList = []

for i in range(1,pageLength+1):
  getResult = getList(i,"ENG",1,1,4)
  data = getResult.get('data',None)
  if data is not None:
    matches = matches + data.get('records',None)
  for match in matches:
    matchInfo = {}
    matchInfo['matchId'] = match.get('id',None)
    matchInfo['regionId'] = match['lg'].get('rid',None)
    matchInfo['regionName'] = match['lg'].get('rnm',None)
    matchInfo['leagueId'] = match['lg'].get('id',None)
    matchInfo['leagueName'] = match['lg'].get('na',None)
    matchInfo['homeTeamId'] = str(match['ts'][0].get('id',None))
    matchInfo['homeTeamIdTrans'] = mapping.get(matchInfo['homeTeamId'],None)
    # print(f'{matchInfo['homeTeamId']} -> {matchInfo['homeTeamIdTrans']}')
    matchInfo['homeTeamName'] = match['ts'][0].get('na',None)
    matchInfo['awayTeamId'] = str(match['ts'][1].get('id',None))
    matchInfo['awayTeamIdTrans'] = mapping.get(matchInfo['awayTeamId'],None)
    matchInfo['awayTeamName'] = match['ts'][1].get('na',None)
    matchList.append(matchInfo)
  print(f"第{i}页已完成,共{pageLength}页")

df_fb = pd.DataFrame(matchList)
df_fb_filtered = df_fb.dropna(subset=['homeTeamIdTrans', 'awayTeamIdTrans'])
df_fb_filtered.to_excel('excel/fb_schedule.xlsx', index=False)

df_hub88 = pd.read_excel('excel/schedule.xlsx')

# 确保数据类型一致
df_hub88['home_team_id'] = df_hub88['home_team_id'].astype(str)
df_hub88['away_team_id'] = df_hub88['away_team_id'].astype(str)
df_fb_filtered['homeTeamIdTrans'] = df_fb_filtered['homeTeamIdTrans'].astype(str)
df_fb_filtered['awayTeamIdTrans'] = df_fb_filtered['awayTeamIdTrans'].astype(str)

# 重命名列名以确保左表的所有列名以FB开头，右表的所有列名以HUB88开头
df_fb_filtered = df_fb_filtered.rename(columns=lambda x: f"FB_{x}")
df_hub88 = df_hub88.rename(columns=lambda x: f"HUB88_{x}")

# 合并 DataFrame
df_merge = pd.merge(df_fb_filtered, df_hub88, left_on=['FB_homeTeamIdTrans', 'FB_awayTeamIdTrans'], right_on=['HUB88_home_team_id', 'HUB88_away_team_id'], how='left')
df_merge.to_excel('excel/schedule_merge.xlsx', index=False)