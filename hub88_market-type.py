import pandas as pd

# 导入 hub88_api 模块
import hub88_api as hub88

df = pd.read_json(r'/Users/wys/dev/hub88-config/pwd.json')

clientId = df['clientId'][0]  # 获取第一行的username
password = df['password'][0]  # 获取第一行的password

print(clientId, password)

token = hub88.get_token(clientId, password)

sports = pd.read_csv('sports.csv')
sportIds = sports['id'].tolist()

market_type = []
i = 0
for sport in sportIds:
    sport_market_type = hub88.get_market_type(token, sport,"False")
    market_type = market_type + sport_market_type
    i += 1
    print(f"{i}/{len(sportIds)}")
# print(market_type)
df_market_type = pd.DataFrame(market_type)

df_market_type = pd.DataFrame(market_type)
print(df_market_type)
df_market_type.to_csv('market_type.csv', index=False, encoding='utf-8')