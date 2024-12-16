import requests
import logging

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
  payload = {
    "sportId": sportId,
    "type": type,
    "hours": hours
  }

  for attempt in range(max_retries):
      try:
          response = requests.get(url, timeout=timeout, json=payload)
          
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

results = getHub88Match(1,2,0,29)
# print(results)
data  = results.get('data', [])
for i in data:
  print(i)
  break