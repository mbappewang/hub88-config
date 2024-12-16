import sys
import os
import requests
import logging
import urllib.parse
import re

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import db
from models import MatchInfo

logger = logging.getLogger(__name__)

def getMatchList(current, languageType, orderBy, type):
    url = "https://sportapi.fastball2.com/v1/match/getList"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6",
        "Authorization": "tt_qCQmf8E7p2aWsWCMsQoS8pbRiAIhXXIK.fe52e300d560390245df7796021eb157",
        "Cache-Control": "no-cache",
        "Content-Type": "application/json;charset=UTF-8",
        "Dnt": "1",
        "Origin": "https://pc1.w.fbs6668.com",
        "Pragma": "no-cache",
        "Referer": "https://pc1.w.fbs6668.com/",
        "Sec-Ch-Ua": "\"Google Chrome\";v=\"131\", \"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": "\"macOS\"",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }


    payload = {

        "current": current,
        "isPC": True,
        "languageType": languageType,
        "orderBy": orderBy,
        "type": type,
    }
    
    max_retries = 10
    timeout = 10
    
    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=timeout)
            
            if response.status_code == 200:
                return response.json()

            logger.error(f"更新LiveMatchList数据失败, 状态码: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"请求LiveMatchList超时，第 {attempt + 1}/{max_retries} 次重试")
        
        except requests.RequestException as e:
            logger.error(f"请求LiveMatchList发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")

    logger.error(f"更新Live数据失败，重试了 {max_retries} 次，仍未成功")
    return None

def getPageTotal(data):
    pageTotal = data.get('pageTotal', 1)
    return pageTotal

def getMatchInfo(data):
    matchList = data.get('records', [])
    if not matchList:
        return []
    matchInfo_list = []
    for match in matchList:
        match_info = {}
        match_info['match_id'] = match.get('id', None)
        match_info['match_name'] = match.get('nm', None)
        animation_list = match.get('as', [])
        match_info['animation_list'] = animation_list
        if not animation_list:
            continue
        else:
            match_info['animation'] = animation_list[0]
        match_info['stream'] = match.get('vs', None)
        matchInfo_list.append(match_info)
    return matchInfo_list

def getStatscore(url,lang,eventId,config_id):
    url = f'https://widgets.statscore.com/api/ssr/render-widget/{config_id}'
    headers = {
        'authority': 'widgets.statscore.com',
        'method': 'GET',
        'scheme': 'https',
        'accept': '*/*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6',
        'cache-control': 'no-cache',
        'dnt': '1',
        'origin': 'https://animation.byanimxyz.com',
        'pragma': 'no-cache',
        'priority': 'u=1, i',
        'referer': 'https://animation.byanimxyz.com/',
        'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    }

    inputData = {
        "language":lang,
        "eventId":str(eventId),
        "timezone":"-480"
    }
    input_data_json = str(inputData).replace("'", '"')
    encoded_data = urllib.parse.quote(input_data_json)
    full_url = f"{url}?inputData={encoded_data}"
    params = {'inputData': inputData}
    
    max_retries = 10
    timeout = 10
    
    for attempt in range(max_retries):
        try:
            response = requests.get(full_url, headers=headers, timeout=timeout)
            
            if response.status_code == 200:
                return response.json()
        
            logger.error(f"更新Statscore数据失败, 状态码: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"请求Statscore超时，第 {attempt + 1}/{max_retries} 次重试")
        
        except requests.RequestException as e:
            logger.error(f"请求Statscore发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")
    
    logger.error(f"更新Statscore数据失败，重试了 {max_retries} 次，仍未成功")
    return None

def getStatscore_id(matchInfo,lang):
    try:
        match = re.search(r'matchId=(\d+)', matchInfo['animation'])
        config = re.search(r'configId=([a-fA-F0-9]+)', matchInfo['animation'])
        if not match or not config:
            logger.error(f"正则匹配 match 或 config 失败: {matchInfo['animation_list']}")
            return None
        match_id = match.group(1)
        config_id = config.group(1)

        Statscore = getStatscore(matchInfo['animation'],'en',match_id,config_id)
        key = f'event|eventId:{match_id}|language:{lang}|timezoneOffset:-480'
        statscore_id = Statscore.get('state', {}).get('fetchHistory', {}).get(key, {}).get('result', {}).get('season', {}).get('stage', {}).get('group', {}).get('event', {}).get('ls_id', None)
        return statscore_id
    except Exception as e:
        logger.error(f"获取Statscore ID失败: {e}")
        return None
    
def insert_matches(insert_list):

    db.session.query(MatchInfo).delete()
    db.session.commit()
    try:
        if insert_list:
            db.session.bulk_insert_mappings(MatchInfo, insert_list)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        logger.error(f'插入失败: {e}')