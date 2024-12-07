import pandas as pd
import hub88_api as hub88
import concurrent.futures
import time

# 读取配置文件
df = pd.read_json(r'pwd.json')
clientId = df['clientId'][0]
password = df['password'][0]

print(clientId, password)

# 获取初始 token
token = hub88.get_token(clientId, password)

# 读取联赛映射文件
df_league = pd.read_json(r'/Users/wys/hub88-config/LeagueMappings.json')
leagues = df_league.to_dict(orient='records')

leaguesdata = []
max_requests_per_second = 20
request_interval = 1 / max_requests_per_second
max_retries = 10

def process_league(league):
    global token
    league_dict = {}
    leagueId = league["id"]
    retries = 0
    while retries < max_retries:
        trans_response = hub88.get_all_translation(token, leagueId, "league")
        if trans_response and type(trans_response) == dict:
            break
        elif trans_response == 401:
            token = hub88.get_token(clientId, password)
        retries += 1
        time.sleep(request_interval)  # 限制请求频率
    if trans_response and type(trans_response) == dict:
        league_dict["id"] = league["id"]
        league_dict["sportId"] = league["sportId"]
        league_dict["locationId"] = league["locationId"]
        league_trans = trans_response['translations']
        for k, v in league_trans.items():
            league_dict[f"league-{k}"] = v
        leaguesdata.append(league_dict)
        print(league_dict)
    else:
        print(f"Failed to get translation for league {leagueId} after {max_retries} retries.")

# 使用 ThreadPoolExecutor 进行多线程处理
with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
    futures = [executor.submit(process_league, league) for league in leagues]
    concurrent.futures.wait(futures)

# 将结果保存到 CSV 文件
df_leagues = pd.DataFrame(leaguesdata)
print(df_leagues)
df_leagues.to_csv('excel/全部leagues多语言.csv', index=False, encoding='utf-8')