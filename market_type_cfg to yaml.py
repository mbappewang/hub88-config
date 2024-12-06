import pandas as pd
import yaml

df = pd.read_excel('/Users/wys/dev/hub88-config/market_type_cfg_副本.xlsx')
data = df.to_dict(orient='records')
data_list = []
for i in data:
    data_dict = {}
    data_dict["sportId"] = int(i["sportId"])
    if int(i["FirstType"]) == 1:
        data_dict["firstMarketTypeId"] = int(i["FirstType"])
        data_dict["firstTypeCount"] = 3
        # data_dict["firstTypeName"] = str(i["FirstTypeName"])
    elif int(i["FirstType"]) == 0:
        data_dict["firstMarketTypeId"] = int(i["FirstType"])
        data_dict["firstTypeCount"] = 0
        # data_dict["firstTypeName"] = ''
    else:
        data_dict["firstMarketTypeId"] = int(i["FirstType"])
        data_dict["firstTypeCount"] = 2
        # data_dict["firstTypeName"] = str(i["FirstTypeName"])

    if int(i["SecondType"]) == 0:
        data_dict["secondMarketTypeId"] = int(i["SecondType"])
        data_dict["secondTypeCount"] = 0
        # data_dict["secondTypeName"] = ''
    else:
        data_dict["secondMarketTypeId"] = int(i["SecondType"])
        data_dict["secondTypeCount"] = 2
        # data_dict["secondTypeName"] = str(i["SecondTypeName"])

    if int(i["ThirdType"]) == 0:
        data_dict["thirdMarketTypeId"] = int(i["ThirdType"])
        data_dict["thirdTypeCount"] = 0
        # data_dict["thirdTypeName"] = ''
    else:
        data_dict["thirdMarketTypeId"] = int(i["ThirdType"])
        data_dict["thirdTypeCount"] = 2
        # data_dict["thirdTypeName"] = str(i["ThirdTypeName"])
    data_list.append(data_dict)

print(data_list)

# 将数据转换为 YAML 格式并保存
save_path = 'market_type_cfg_copy.yaml'
with open(save_path, 'w', encoding='utf-8') as f:
    yaml.dump(data_list, f, 
    allow_unicode=True,  # 支持中文
    default_flow_style=False,  # 使用块状格式
    sort_keys=False,  # 不对键进行排序
    indent=2)  # 设置缩进为2个字符

# 将数据转换为 DataFrame 并保存为 Excel 文件
# df_output = pd.DataFrame(data)
# save_path_excel = 'market_type_cfg.xlsx'
# df_output.to_excel(save_path_excel, index=False)

# 将数据转换为 DataFrame 并保存为 json 文件
# df_output = pd.DataFrame(data_list)
# save_path_json = 'market_type_cfg.json'
# df_output.to_json(save_path_json, orient='records')