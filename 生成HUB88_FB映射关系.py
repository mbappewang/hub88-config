import requests
import json
import pandas as pd
import logging
import urllib.parse
import re
import datetime

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,  # 设置最低日志级别为INFO
    format='%(asctime)s.%(msecs)03d %(levelname)s [%(name)s] %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 设置时间格式
    handlers=[
        logging.StreamHandler(),  # 只添加控制台输出handler
        logging.FileHandler('Log/hub88_fb.log')  # 添加文件处理器
    ]
)

# 获取logger实例
logger = logging.getLogger(__name__)

# 测试日志输出
logger.info("程序开始运行")
logger.error("这是一条测试错误信息")

def getList(current,languageType,orderBy,type):
    url = "https://api.fastbsv.com/v1/match/getList"

    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,ja;q=0.7,id;q=0.6",
        "Authorization": "tt_qqWy6dXJ7WG0gAEDG1B6vabsCtuIoMWO.bc8945c114c71dc0d624ba290a35826d",
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
    "isPc":False,
    "languageType":languageType,
    "orderBy":orderBy,
    "type":type
    }
    max_retries = 10
    timeout = 10

    for attempt in range(max_retries):
        try:
            response = requests.post(url, headers = headers, json=payload, timeout=timeout)
            
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
        match_info['match_time'] = match.get('bt', None)
        match_info['regionName'] = match.get('lg', None).get('rnm', None)
        match_info['regionId'] = match.get('lg', None).get('rid', None)
        match_info['regionUrl'] = match.get('lg', None).get('rlg', None)
        match_info['leagueName'] = match.get('lg', None).get('na', None)
        match_info['leagueId'] = match.get('lg', None).get('id', None)
        match_info['leagueUrl'] = match.get('lg', None).get('lurl', None)
        match_info['match_id'] = match.get('id', None)
        match_info['match_name'] = match.get('nm', None)
        match_info['homeTeam'] = match.get('ts', None)[0]['na']
        match_info['homeTeamUrl'] = match.get('ts', None)[0]['lurl']
        match_info['homeTeamId'] = match.get('ts', None)[0]['id']
        match_info['awayTeam'] = match.get('ts', None)[1]['na']
        match_info['awayTeamUrl'] = match.get('ts', None)[1]['lurl']
        match_info['awayTeamId'] = match.get('ts', None)[1]['id']
        animation_list = match.get('as', [])
        match_info['animation_list'] = animation_list
        if not animation_list:
            continue
        elif len(animation_list) == 1:
            match_info['animation1'] = None
            match_info['animation2'] = animation_list[0]
        elif len(animation_list) == 2:
            match_info['animation1'] = animation_list[0]
            match_info['animation2'] = animation_list[1]
        match_info['flvHD'] = match.get('vs', None).get('web', None)
        match_info['flvHD'] = match.get('vs', None).get('flvHD', None)
        match_info['flvSD'] = match.get('vs', None).get('flvSD', None)
        match_info['m3u8HD'] = match.get('vs', None).get('m3u8HD', None)
        match_info['m3u8SD'] = match.get('vs', None).get('m3u8SD', None)
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
        if matchInfo['animation1'] is None:
            logger.info(f"animation1为空")
            statscore_id = 0
            return statscore_id
        startTime = datetime.datetime.now()
        match = re.search(r'matchId=(\d+)', matchInfo['animation1'])
        config = re.search(r'configId=([a-fA-F0-9]+)', matchInfo['animation1'])
        if not match or not config:
            # logger.error(f"正则匹配 match 或 config 失败: {matchInfo['animation_list']}")
            return None
        match_id = match.group(1)
        config_id = config.group(1)
        Statscore = getStatscore(matchInfo['animation1'],'en',match_id,config_id)
        key = f'event|eventId:{match_id}|language:{lang}|timezoneOffset:-480'
        statscore_id = Statscore.get('state', {}).get('fetchHistory', {}).get(key, {}).get('result', {}).get('season', {}).get('stage', {}).get('group', {}).get('event', {}).get('ls_id', None)
        endTime = datetime.datetime.now()
        logger.info(f"获取Statscore ID成功: {statscore_id} 用时{endTime - startTime}")
        return statscore_id
    except Exception as e:
        logger.error(f"获取Statscore ID失败: {e}")
        return None

try:
    pageTotal  = 1
    results = getList(1, 'CMN', 1,4)
    data = results.get('data', {})
    pageTotal = getPageTotal(data)
    logger.info(f"Get pageTotal: {pageTotal}")
except Exception as e:
    logger.error(f"Error get pageTotal: {e}")
matchInfo_list = []
for current in range(1, pageTotal+1):
    logger.info(f"current: {current}")
    results = getList(current, 'CMN', 1,4)
    data = results.get('data', {})
    if not data:
        continue
    matchInfo_list = matchInfo_list +  getMatchInfo(data)
logger.info(f"Get {len(matchInfo_list)} matches")
matchInfo_list_finial = []
for matchInfo in matchInfo_list:
    statscore_id = getStatscore_id(matchInfo,'en')
    if statscore_id is None:
        continue
    matchInfo['statscore_id'] = statscore_id
    matchInfo_list_finial.append(matchInfo)
logger.info(f"Get {len(matchInfo_list_finial)} matches with statscore_id")
for i in matchInfo_list:
    print(i)

