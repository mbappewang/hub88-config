import pandas as pd

# 导入 hub88_api 模块
import hub88_api as hub88

df = pd.read_json(r'/Users/wys/hub88-config/pwd.json')

clientId = df['clientId'][0]  # 获取第一行的username
password = df['password'][0]  # 获取第一行的password

print(clientId, password)

token = hub88.get_token(clientId, password)

df_regions = pd.read_json(r'/Users/wys/hub88-config/LocationMappings.json')

regions = df_regions['id'].tolist()
regionsdata = []
for region in regions:
    region_dict = {}
    trans_response = hub88.get_all_translation(token, region, "region")
    region_dict["id"] = region
    print(trans_response)
    region_trans = trans_response['translations']
    # print(sport_trans)
    for k,v in region_trans.items():
        region_dict[f"region-{k}"] = v
    regionsdata.append(region_dict)
    print(region_dict)
    # break

df_regions = pd.DataFrame(regionsdata)
print(df_regions)
df_regions.to_csv('regions.csv', index=False, encoding='utf-8')