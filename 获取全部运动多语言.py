import pandas as pd

# 导入 hub88_api 模块
import hub88_api as hub88

df = pd.read_json(r'pwd.json')

clientId = df['clientId'][0]  # 获取第一行的username
password = df['password'][0]  # 获取第一行的password

print(clientId, password)

token = hub88.get_token(clientId, password)

sports = hub88.get_sports(token)
df = pd.DataFrame(sports)
sportIds = df['id'].tolist()
sportsdata = []
for sport in sportIds:
    sport_dict = {}
    trans_response = hub88.get_all_translation(token, sport, "sport")
    sport_dict["id"] = sport
    sport_trans = trans_response['translations']
    # print(sport_trans)
    for k,v in sport_trans.items():
        sport_dict[f"sport-{k}"] = v
    sportsdata.append(sport_dict)
    print(sport_dict)
    # break

df_sports = pd.DataFrame(sportsdata)
print(df_sports)
df_sports.to_csv('excel/全部sports翻译.csv', index=False, encoding='utf-8')