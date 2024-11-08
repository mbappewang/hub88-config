import pandas as pd
import random
import yaml

# 导入 hub88_api 模块
import hub88_api as hub88

df = pd.read_json(r'/Users/wys/hub88-config/pwd.json')

clientId = df['clientId'][0]  # 获取第一行的username
password = df['password'][0]  # 获取第一行的password

# print(clientId, password)

token = hub88.get_token(clientId, password)


def get_market_dict(token,eventId):
  event = hub88.get_eventInfo(token, eventId)
  df_event = pd.DataFrame(event['markets'])
  save_path = r'/Users/wys/hub88-config/event.json'
  df_event.to_json(save_path, orient='records', force_ascii=False, indent=4)

  # 过滤 trading_status = 1 的行
  df_event_filtered = df_event[df_event['tradingStatus'] == 0]

  # 按 id 列升序排序
  df_event_filtered = df_event_filtered.sort_values(by='id', ascending=True)

  # 创建一个列表存储结果
  marketId_list = []

  # 获取排序后的 id 列表
  id_list = df_event_filtered['id'].tolist()

  # 处理不同情况
  if len(id_list) == 0:
      marketId_1 = 0
      marketId_2 = 0
  elif len(id_list) == 1:
      marketId_1 = id_list[0]
      marketId_2 = 0
  else:
      marketId_1 = id_list[0]
      marketId_2 = id_list[1]
  return marketId_1,marketId_2

df_eventIds = pd.read_csv(r'/Users/wys/hub88-config/schedule_filtered.csv')
dict_data = df_eventIds[['id', 'sport_id']].to_dict(orient='records')
# print(dict_data)
# break
tag_list = []
i = 0
tag_dict = {
   457:["2nd refund","20% Cashback","BOG"],
   0:["Best Odds","50% Freebet","100% Freebet","100% Cashback"]
}

def get_tag(sport_id):
  if sport_id == 457:
    max = len(tag_dict[sport_id])
    idx1, idx2 = random.sample(range(max), 2)
    return tag_dict[sport_id][idx1], tag_dict[sport_id][idx2]
  else:
    sport_id = 0
    max = len(tag_dict[sport_id])
    idx1, idx2 = random.sample(range(max), 2)
    return tag_dict[sport_id][idx1], tag_dict[sport_id][idx2]

for event in dict_data:
  event_id = event['id']
  sport_id = event['sport_id']
  marketId_1,marketId_2 = get_market_dict(token, event_id)
  tag_1,tag_2 = get_tag(sport_id)
  event_dict_1 = {'eventId': event_id, 'sportId': sport_id, 'marketId': marketId_1, 'tag': tag_1}
  event_dict_2 = {'eventId': event_id, 'sportId': sport_id, 'marketId': marketId_2, 'tag': tag_2}
  tag_list.append(event_dict_1)
  tag_list.append(event_dict_2)
  event_dict_1 = {}
  event_dict_2 = {}
  i += 1
  print(f"{i}/{len(dict_data)}")
  # if i == 5:
  #   break
# print(tag_list)
df_tag = pd.DataFrame(tag_list)
# print(df_tag)
save_path = r'/Users/wys/hub88-config/tag.json'
df_tag.to_json(save_path, orient='records', force_ascii=False, indent=4)

df_yaml = pd.read_json(r'/Users/wys/hub88-config/tag.json')
df_yaml = df_yaml[['eventId', 'marketId', 'tag']]
df_yaml = df_yaml[df_yaml['marketId'] != 0]

# 3. 将数据转换为 YAML 格式并保存
save_path = r'/Users/wys/hub88-config/tag.yaml'

# 方法1：使用 DataFrame
with open(save_path, 'w', encoding='utf-8') as f:
  yaml.dump(df_yaml.to_dict(orient='records'), f, 
  allow_unicode=True,  # 支持中文
  default_flow_style=False,  # 使用块状格式
  sort_keys=False)  # 不对键进行排序