import pandas as pd
import yaml

# 导入 hub88_api 模块
import hub88_api as hub88

df = pd.read_json(r'pwd.json')

clientId = df['clientId'][0]  # 获取第一行的username
password = df['password'][0]  # 获取第一行的password

# print(clientId, password)

token = hub88.get_token(clientId, password)



df_sports = pd.read_csv('schedule_filtered.csv')
df_sports = df_sports[df_sports['competition_id'].isin([8655,33,1,29,28])]
eventIds = df_sports['id'].tolist()

banners = []
i = 0
for event in eventIds:
  try:
    banner = {}
    market = hub88.get_eventInfo(token, event)
    market_1x2 = [m for m in market['markets'] if m['name'] == '1x2' and m['tradingStatus'] == 0]
    banner["eventId"] = event
    print(event)
    banner["marketId"] = market_1x2[0]['id']
    banner["leagueId"] = market['eventInfo']['competition']['id']
    banner["image"] = f"https://assets.wintokens.io/webpage/sports/banners/{market['eventInfo']['competition']['id']}.png"
    banner["away"] = market['eventInfo']['competitors'][1]['name']
    banner["home"] = market['eventInfo']['competitors'][0]['name']
    banners.append(banner)
    i += 1
    print(f"{i}/{len(eventIds)}")
  except:
    print(f"获取eventInfo失败, eventId: {event}")
  # break
# print(banners)
df_yaml = pd.DataFrame(banners)
# print(df_yaml)

# yaml_data = {'homeBanner': df_yaml.to_dict(orient='records')}
data = df_yaml.to_dict(orient='records')
# 将数据转换为 YAML 格式并保存
save_path = r'yaml/homeBanner.yaml'
with open(save_path, 'w', encoding='utf-8') as f:
  yaml.dump(data, f, 
  allow_unicode=True,  # 支持中文
  default_flow_style=False,  # 使用块状格式
  sort_keys=False,  # 不对键进行排序
  indent=2)  # 设置缩进为2个字符