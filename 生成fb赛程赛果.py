import pandas as pd
import requests

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

responesResult = getResults(1733673600000, 1733759999999, "ENG", 1)
data = responesResult.get('data', None)
if data is not None:
    matches = data.get('data', None)
