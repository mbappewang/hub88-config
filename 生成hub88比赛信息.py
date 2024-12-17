import requests
import logging
from hub88_api import get_token,get_metadata
import re
import pandas as pd
import time

# 配置日志系统
logging.basicConfig(
    level=logging.INFO,  # 设置最低日志级别为INFO
    format='%(asctime)s.%(msecs)03d %(levelname)s [%(name)s] %(message)s',  # 设置日志格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 设置时间格式
    handlers=[
        logging.StreamHandler(),  # 只添加控制台输出handler
        logging.FileHandler('Log/hub88_metadata.log')  # 添加文件处理器
    ]
)

# 获取logger实例
logger = logging.getLogger(__name__)

# 测试日志输出
logger.info("程序开始运行")
logger.error("这是一条测试错误信息")

def getHub88Sport():
  url = "https://bet-hub88.prod.wintokens.io/hub88/sportsData"
  max_retries = 10
  timeout = 10

  for attempt in range(max_retries):
      try:
          response = requests.get(url, timeout=timeout)
          
          if response.status_code == 200:
              return response.json()

          logger.error(f"更新LiveMatchList数据失败, 状态码: {response.status_code}")
      
      except requests.Timeout:
          logger.error(f"请求LiveMatchList超时，第 {attempt + 1}/{max_retries} 次重试")
      
      except requests.RequestException as e:
          logger.error(f"请求LiveMatchList发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")

  logger.error(f"更新Live数据失败，重试了 {max_retries} 次，仍未成功")
  return None

def getHub88League(sportId,type,hours):
  url = "https://bet-hub88.prod.wintokens.io/hub88/league"
  max_retries = 10
  timeout = 10
  params = {
    "sportId": sportId,
    "type": type,
    "hours": hours
  }

  for attempt in range(max_retries):
      try:
          response = requests.get(url, timeout=timeout, params=params)
          
          if response.status_code == 200:
              return response.json()

          logger.error(f"更新LiveMatchList数据失败, 状态码: {response.status_code}")
      
      except requests.Timeout:
          logger.error(f"请求LiveMatchList超时，第 {attempt + 1}/{max_retries} 次重试")
      
      except requests.RequestException as e:
          logger.error(f"请求LiveMatchList发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")

  logger.error(f"更新Live数据失败，重试了 {max_retries} 次，仍未成功")
  return None

def getHub88Match(sportId,type,hours,leagueId):
    url = "https://bet-hub88.prod.wintokens.io/hub88/league/matches"
    max_retries = 10
    timeout = 10
    params = {
    "sportId": sportId,
    "type": type, 
    "hours": hours,
    "leagueId": leagueId
    }

    for attempt in range(max_retries):
        try:
            response = requests.get(url, timeout=timeout, params=params)
            
            if response.status_code == 200:
                return response.json()

            logger.error(f"更新LiveMatchList数据失败, 状态码: {response.status_code}")
        
        except requests.Timeout:
            logger.error(f"请求LiveMatchList超时，第 {attempt + 1}/{max_retries} 次重试")
        
        except requests.RequestException as e:
            logger.error(f"请求LiveMatchList发生错误：{e}, 第 {attempt + 1}/{max_retries} 次重试")

    logger.error(f"更新Live数据失败，重试了 {max_retries} 次，仍未成功")
    return None

def getStatscoreId(datalist):
    for i in datalist:
        if i['dataType'] == 'StatsCoreIntegration':
            return i.get('data', None).get('Id', None)
    return None

def extract_number(text):
    match = re.search(r'm:(\d+)', text)
    if match:
        return match.group(1)
    return None

def getHub88data(token,sportId,type,hours,leagueId):
    results = getHub88Match(sportId,type,hours,leagueId)
    # print(results)
    data  = results.get('data', [])
    if not data:
        return []
    eventList = []
    for i in data:
        eventInfo = {}
        eventInfo['sportId'] = i.get('sportId', None)
        eventInfo['leagueId'] = i.get('leagueId', None)
        eventInfo['locationId'] = i.get('locationId', None)
        eventInfo['hometeam'] = i['eventInfo'].get('competitors', None)[0]['name']
        eventInfo['hometeamId'] = i['eventInfo'].get('competitors', None)[0]['id']
        eventInfo['awayteam'] = i['eventInfo'].get('competitors', None)[1]['name']
        eventInfo['awayteamId'] = i['eventInfo'].get('competitors', None)[1]['id']
        eventInfo['startTime'] = i.get('startTime', None)
        eventInfo['eventId'] = i.get('eventId', None)
        logger.info(f"Wintokens 数据请求成功: {i.get('eventName', None)}")
        eventInfo['statscoreId'] = extract_number(getStatscoreId(get_metadata(token,i['eventId'])))
        logger.info(f"hub88 - metadata: {i.get('eventName', None)}")
        eventList.append(eventInfo)
    return eventList

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

def upsert_to_database(df, engine, table_name, primary_key):
    try:
        existing_ids = pd.read_sql(f"SELECT {primary_key} FROM {table_name}", engine)[primary_key].tolist()
        
        df_update = df[df[primary_key].isin(existing_ids)]
        df_insert = df[~df[primary_key].isin(existing_ids)]
        
        # 更新已存在的记录
        if not df_update.empty:
            with engine.connect() as connection:
                for index, row in df_update.iterrows():
                    update_cols = [col for col in df.columns if col != primary_key]
                    update_stmt = text(f"""
                        UPDATE {table_name} 
                        SET {', '.join([f"{col} = :{col}" for col in update_cols])}
                        WHERE {primary_key} = :{primary_key}
                    """)
                    
                    # 构建参数字典
                    params = {col: row[col] for col in df.columns}
                    connection.execute(update_stmt, params)
                connection.commit()
                logger.info(f"更新了 {len(df_update)} 条记录")
        
        # 追加新记录
        if not df_insert.empty:
            df_insert.to_sql(table_name, con=engine, if_exists='append', index=False)
            logger.info(f"插入了 {len(df_insert)} 条记录")
            
        return True
        
    except SQLAlchemyError as e:
        logger.error(f"数据库操作错误: {str(e)}")
        return False
while True:
    logger.info("开始运行")
    # 读取配置文件
    df = pd.read_json(r'pwd.json')
    clientId = df['clientId'][0]
    password = df['password'][0]
    token = get_token(clientId, password)
    sportIds = [1,8,11,4,25,4,14,23,94,6,589,17,622,7,35,57]
    typeIds = [1]
    # # getHub88data(token,sportId,type,hours,leagueId):
    # df = pd.DataFrame(getHub88data(token,1,2,0,29))

    # # 创建数据库连接
    # engine = create_engine('mysql+pymysql://sportData:syrJBBSPT67At4rs@34.84.102.182:3306/sportdata')
    # # upsert_to_database(df, engine, table_name, primary_key):
    # upsert_to_database(df, engine,'hub88','eventId')
    for sportId in sportIds:
        logger.info(f"开始请求sportId: {sportId}")
        for typeId in typeIds:
            logger.info(f"开始请求typeId: {typeId}")
            resultsdata = getHub88League(sportId,typeId,0)
            data = resultsdata.get('data', [])
            if not data:
                continue
            leagueIds = [i.get('leagueId', None) for i in data]
            print(len(leagueIds),leagueIds)
            for leagueId in leagueIds:
                logger.info(f"开始请求leagueId: {leagueId}")
                data = getHub88data(token,sportId,typeId,0,leagueId)
                if not data:
                    continue
                df = pd.DataFrame(data)
                engine = create_engine('mysql+pymysql://sportData:syrJBBSPT67At4rs@34.84.102.182:3306/sportdata')
                upsert_to_database(df, engine,'hub88','eventId')
    logger.info("等待15分钟")
    time.sleep(15*60)

