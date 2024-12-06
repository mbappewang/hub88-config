import pandas as pd
import yaml

# 读取 Excel 文件
df = pd.read_excel('hot league.xlsx')

# 将 league_hot_row_num 列转换为数值类型，无法转换的值将被设置为 NaN
df['league_hot_row_num'] = pd.to_numeric(df['league_hot_row_num'], errors='coerce')

# 过滤掉 league_hot_row_num 列中值为 NaN 的行
df_filtered = df.dropna(subset=['league_hot_row_num'])
league_list = [7200, 6763, 53, 349, 9574, 68354, 215, 205, 1411, 358, 1216, 4276, 589, 33, 4830, 465, 471, 854, 100, 35, 514, 4194, 9935, 8655, 503, 884, 489, 4207, 8635, 28, 8599, 520, 508, 29, 9436, 293, 250, 494, 7104, 1, 9479, 99, 221, 397, 98, 191, 190, 1141, 392, 192, 554]
df_filtered = df_filtered[df_filtered['league_id'].isin(league_list)]
# 按 league_hot_row_num 列进行排序
df_sorted = df_filtered.sort_values(by='league_hot_row_num')

# 将数据转换为字典格式
data = df_sorted.to_dict(orient='records')
hot_item = {}
hot_league = []

# 遍历数据并构建 hot_league 列表
for i in data:
    hot_item = {}
    hot_item["leagueId"] = i["league_id"]
    hot_item["sportId"] = i["sportId"]
    hot_league.append(hot_item)

print(hot_league)

# 将数据转换为 YAML 格式并保存
save_path = 'yaml/top_league.yaml'
with open(save_path, 'w', encoding='utf-8') as f:
    yaml.dump(hot_league, f, 
    allow_unicode=True,  # 支持中文
    default_flow_style=False,  # 使用块状格式
    sort_keys=False,  # 不对键进行排序
    indent=2)  # 设置缩进为2个字符