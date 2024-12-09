import pandas as pd
import requests
import pytz
from datetime import datetime
from sqlalchemy import create_engine
import mysql.connector

def getResults(beginTime, endTime, languageType, sportId):
    url = f'https://sportapi.fastball2.com/v1/match/matchResultList'
    payload = {
        "beginTime": beginTime,
        "endTime": endTime,
        "languageType": languageType,
        "sportId": sportId,
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"获取schedule失败,状态码: {response.status_code}")
        print("响应内容:", response.text)
        return response.status_code

def resultParse(matchDict):
    matchInfo = {}
    matchInfo['startTime'] = matchDict.get('bt', None)
    matchInfo['sportId'] = matchDict.get('sid', None)
    matchInfo['FB_match_id'] = matchDict.get('id', None)
    matchInfo['regionId'] = matchDict['lg'].get('rid', None)
    matchInfo['regionName'] = matchDict['lg'].get('rnm', None)
    matchInfo['regionImage'] = matchDict['lg'].get('rlg', None)
    matchInfo['leagueId'] = matchDict['lg'].get('id', None)
    matchInfo['leagueName'] = matchDict['lg'].get('na', None)
    matchInfo['leagueImage'] = matchDict['lg'].get('lurl', None)
    matchInfo['homeTeamId'] = str(matchDict['ts'][0].get('id', None))
    matchInfo['homeTeamName'] = matchDict['ts'][0].get('na', None)
    matchInfo['homeTeamImage'] = matchDict['ts'][0].get('lurl', None)
    matchInfo['awayTeamId'] = str(matchDict['ts'][1].get('id', None))
    matchInfo['awayTeamName'] = matchDict['ts'][1].get('na', None)
    matchInfo['awayTeamImage'] = matchDict['ts'][1].get('lurl', None)
    return matchInfo

def one_day_result(beginTime, endTime):
    responesResult = getResults(beginTime, endTime, "ENG", 1)
    data = responesResult.get('data', None)
    matchesinfo = []
    if data is not None:
        for match in data:
            matchInfo = resultParse(match)
            matchesinfo.append(matchInfo)
    return matchesinfo

def getUnixTime(date):
    local_timezone = pytz.timezone('Asia/Shanghai')
    local_time = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    local_time_with_tz = local_timezone.localize(local_time)
    utc_time = local_time_with_tz.astimezone(pytz.utc)
    unix_timestamp_with_ms = int(utc_time.timestamp() * 1000)
    return unix_timestamp_with_ms

startDate = '2023-12-10 00:00:00'
searchDate = 365
beginTime = getUnixTime(startDate)

# MySQL 数据库配置
db_config = {
    'user': 'sportData',
    'password': 'syrJBBSPT67At4rs',
    'host': '34.84.102.182',
    'database': 'sportdata'
}
# 创建数据库连接引擎
engine = create_engine(f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}")

for i in range(0, searchDate):
    beginTime = beginTime + i * 86400000
    endTime = beginTime + 86400000
    matchesinfo = one_day_result(beginTime, endTime)
    df = pd.DataFrame(matchesinfo)
    # 遍历 DataFrame 的每一行并插入到 MySQL 数据库
    try:
        # 尝试将整个 DataFrame 插入到 MySQL 数据库
        df.to_sql('fb_data', con=engine, if_exists='append', index=False)
        print(f"第{i+1}日数据已保存")
    except Exception as e:
        print(f"第{i+1}日数据批量插入失败，尝试每50行插入")
        print(e)
        # 如果批量插入失败，尝试每50行插入
        for j in range(0, len(df), 50):
            df_chunk = df.iloc[j:j+50]
            try:
                df_chunk.to_sql('fb_data', con=engine, if_exists='append', index=False)
                print(f"第{i+1}日第{j//50+1}批数据已保存")
            except Exception as e:
                print(f"第{i+1}日第{j//50+1}批数据插入失败，尝试逐行插入")
                print(e)
                # 如果每50行插入失败，逐行插入
                for index, row in df_chunk.iterrows():
                    try:
                        row.to_frame().T.to_sql('fb_data', con=engine, if_exists='append', index=False)
                        print(f"第{i+1}日第{index+1}行数据已保存")
                        print(row)
                    except Exception as e:
                        print(f"第{i+1}日第{index+1}行数据保存失败")
                        print(e)

