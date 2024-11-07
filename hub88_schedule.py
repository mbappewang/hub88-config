import pandas as pd

# 导入 hub88_api 模块
import hub88_api as hub88

df = pd.read_json(r'C:\Users\wys94\hub88 config\pwd.json')

clientId = df['clientId'][0]  # 获取第一行的username
password = df['password'][0]  # 获取第一行的password

print(clientId, password)

token = hub88.get_token(clientId, password)

startDate_list = ["2024-11-09","2024-11-10","2024-11-11"]
sportIds = [1,8,7,4,14,11,17,25,457,6]
locationIds = [66,25,22,23,1,59]
schedule = []
for startDate in startDate_list:
    data = hub88.get_schedule(token, startDate, sportIds, locationIds)
    schedule = schedule + data
df_schedule = pd.DataFrame(schedule)
save_path = r'C:\Users\wys94\hub88 config\schedule.json'
df_schedule.to_json(save_path, orient='records', force_ascii=False, indent=4)

# 读取 JSON 文件
df = pd.read_json('schedule.json')

# 使用 json_normalize 展平数据
df_flat = pd.json_normalize(
    df.to_dict('records'),
    sep='_',
    # 定义要展平的字段和路径
    meta=[
        'id', 'name', 'status', 'tradingStatus',
        ['country', 'id'], ['country', 'name'],
        ['sport', 'id'], ['sport', 'name'],
        ['competition', 'id'], ['competition', 'name'],
        'startTime', 'isOutright'
    ]
)

# 处理 competitors 数组
df_flat['home_team_id'] = df.apply(lambda x: x['competitors'][0]['id'], axis=1)
df_flat['home_team_name'] = df.apply(lambda x: x['competitors'][0]['name'], axis=1)
df_flat['away_team_id'] = df.apply(lambda x: x['competitors'][1]['id'], axis=1)
df_flat['away_team_name'] = df.apply(lambda x: x['competitors'][1]['name'], axis=1)

# 保存结果
df_flat.to_csv('schedule_flat.csv', index=False)

# 过滤 trading_status = 1 的行
df_filtered = df_flat[df_flat['tradingStatus'] == 0]

# 保存过滤后的结果
df_filtered.to_csv('schedule_filtered.csv', index=False)

# 如果需要查看结果
print(f"全部比赛数: {len(df_flat)}")
print(f"可交易比赛数: {len(df_filtered)}")