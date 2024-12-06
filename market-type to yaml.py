import pandas as pd
import yaml

df = pd.read_csv('market_type_副本.csv')
data = df.to_dict(orient='records')
market_type_cfg = []
market_type = {}
sportIdbefore = None
sportIds = [457,7,1,8,14,11,4,2,6,622,17,25,1183,16,94,23,9,35,54,51,52,53,20,48,5,49,27,33,18,41,42,39,589,28,38,721,56,57,58,21,60,12,13,59,19,22,29,34,40,15,160,193,26,30,37,43,45,47,61,62,63,127,1117,886,1381]
for i in data:
    if i["sportId"] not in sportIds:
        continue
    sportIdnow = i["sportId"]
    if sportIdnow != sportIdbefore:
        if market_type:
            market_type_cfg.append(market_type)
        market_type = {}
    market_type["sportId"] = i["sportId"]
    market_type["sportName"] = i["sportName"]
    if pd.notna(i["First"]):
        market_type["FirstType"] = i["id"]
        market_type["FirstTypeName"] = i["name"]
    elif pd.notna(i["second"]):
        market_type["SecondType"] = i["id"]
        market_type["SecondTypeName"] = i["name"]
    elif pd.notna(i["third"]):
        market_type["ThirdType"] = i["id"]
        market_type["ThirdTypeName"] = i["name"]
    sportIdbefore = sportIdnow

# 添加最后一个 market_type
if market_type:
    market_type_cfg.append(market_type)

print(market_type_cfg)

# 将数据转换为 YAML 格式并保存
save_path = 'market_type_cfg.yaml'
with open(save_path, 'w', encoding='utf-8') as f:
    yaml.dump(market_type_cfg, f, 
    allow_unicode=True,  # 支持中文
    default_flow_style=False,  # 使用块状格式
    sort_keys=False,  # 不对键进行排序
    indent=2)  # 设置缩进为2个字符

# 将数据转换为 DataFrame 并保存为 Excel 文件
df_output = pd.DataFrame(market_type_cfg)
save_path_excel = 'market_type_cfg.xlsx'
df_output.to_excel(save_path_excel, index=False)