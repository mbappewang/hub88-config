import pandas as pd
from datetime import datetime, timedelta
import yaml
# 导入 hub88_api 模块
import hub88_api as hub88

# 读取密码
df = pd.read_json(r'pwd.json')
clientId = df['clientId'][0]  # 获取第一行的username
password = df['password'][0]  # 获取第一行的password
# 获得token
token = hub88.get_token(clientId, password)
if token:
  print("获取token成功")
else:
  print("获取token失败")

# 指定赛程参数: 运动，日期（前闭后闭），地区
sportIds = [1]
# UTC0日期
start_date = datetime(2024, 12, 12)
end_date = datetime(2024, 12, 31)
# 地区可不填
locationIds = []

# 生成时间list
startDate_list = []
current_date = start_date
while current_date <= end_date:
    startDate_list.append(current_date.strftime('%Y-%m-%d'))
    current_date += timedelta(days=1)

# 请求赛程
schedule = []
for startDate in startDate_list:
    print(startDate)
    data = hub88.get_schedule(token, startDate, sportIds, locationIds)
    schedule = schedule + data
# 响应体data 例子
# [
#     {
#         "id": 6605093,
#         "name": "Arsenal LFC v Aston Villa Lfc",
#         "status": 1,
#         "tradingStatus": 1,
#         "statusDescription": null,
#         "country": {
#             "id": 25,
#             "name": "England"
#         },
#         "sport": {
#             "id": 1,
#             "name": "Soccer"
#         },
#         "competition": {
#             "id": 749,
#             "name": "The FA Women&apos;s Super League"
#         },
#         "season": null,
#         "competitors": [
#             {
#                 "id": 24075,
#                 "name": "Arsenal LFC"
#             },
#             {
#                 "id": 31968,
#                 "name": "Aston Villa Lfc"
#             }
#         ],
#         "startTime": "2024-12-08T14:00:00",
#         "isOutright": false,
#         "customDisplayData": {},
#         "isBetBuilderSupported": false
#     },
#     {}
# ]
 
# 展平df
df = pd.DataFrame(schedule)
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
df_flat = df_flat.drop(columns=["competitors"])

# 初步筛选出热门league
df_filtered = df_flat[df_flat['competition_id'].isin([1,28,29,33,191])]

# 热门球队id
# [{'10787':'Borussia Dortmund'},{'10913':'AC Milan'},{'10170':'FC Barcelona'},{'11026':'Real Madrid'},{'10938':'Tottenham Hotspur'},{'10148':'Chelsea FC'},{'10936':'Liverpool FC'},{'10927':'Manchester United'},{'10718':'Arsenal FC'},{'10929':'Everton FC'},{'10883':'Manchester City'},{'10917':'Inter Milano'},{'10863':'Juventus Turin'},{'10770':'FC Bayern Munich'}]
team_ids = [10787,10913,10170,11026,10938,10148,10936,10927,10718,10929,10883,10917,10863,10770]

# 精筛热门球队
df_filtered = df_filtered[
    (df_filtered['home_team_id'].isin(team_ids)) | (df_filtered['away_team_id'].isin(team_ids))
]

# 不要Outright
df_filtered = df_filtered[df_filtered['isOutright'] == False]

# df_filtered = df_filtered.to_excel('excel/schedule.xlsx', index=False)

# 遍历筛选结果，生成配置
banner_events = df_filtered.to_dict(orient='records')
banner_list = []
for i in banner_events:
   banner = {}
   banner["eventId"] = i['id']
   banner["marketId"] = 1
   banner["leagueId"] = i['competition_id']
   banner["image"] = f"https://assets.wintokens.io/webpage/sports/banners/{i['competition_id']}.png"
   banner["away"] = i['away_team_name']
   banner["home"] = i['home_team_name']
   banner_list.append(banner)

# 保存为yaml
save_path = r'yaml/hub88_home_banner.yaml'
with open(save_path, 'w', encoding='utf-8') as f:
  yaml.dump(banner_list, f, 
  allow_unicode=True,  # 支持中文
  default_flow_style=False,  # 使用块状格式
  sort_keys=False,  # 不对键进行排序
  indent=2)  # 设置缩进为2个字符