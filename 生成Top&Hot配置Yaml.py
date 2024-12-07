import pandas as pd
import yaml
import os

# Top League 需要在首页展示Svg资源，所以需确认是否目前有这个资源
# 而Hot League 只影响比赛列表页的排序，不需要确认资源是否存在

def get_all_filenames_without_extension(folder_path):
    filenames_without_extension = []
    # 遍历指定文件夹中的所有文件
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            # 检查文件后缀名，如果不是 svg 则跳过
            if not file.endswith('.svg'):
                continue
            # 获取文件名，不包含后缀
            filename_without_extension = os.path.splitext(file)[0]
            filenames_without_extension.append(filename_without_extension)
    return filenames_without_extension

def parse_filenames(filenames):
    parsed_data = []
    for filename in filenames:
        # 分割文件名，提取 sportId 和 leagueId
        sportId, leagueId = filename.split('-')
        parsed_data.append({
            'leagueId': int(leagueId),
            'sportId': int(sportId)
        })
    return parsed_data

def create_data(data):
    item = {}
    league = []
    for i in data:
      item = {}
      item["leagueId"] = i["league_id"]
      item["sportId"] = i["sportId"]
      league.append(item)
    return league

# 获取已有的Svg资源,存为topLeague_list
folder_path = "Top League Svg"
filenames = get_all_filenames_without_extension(folder_path)
parsed_data = parse_filenames(filenames)
df_topLeagues = pd.DataFrame(parsed_data)
topLeague_list = df_topLeagues['leagueId'].tolist()
print(topLeague_list)

# 读取配置的excel文件
df = pd.read_excel(r'excel/League_config.xlsx')
# 将 league_hot_row_num 列转换为数值类型，无法转换的值将被设置为 NaN
df['league_hot_row_num'] = pd.to_numeric(df['league_hot_row_num'], errors='coerce')
# 过滤掉 league_hot_row_num 列中值为 NaN 的行
# 获得hot league 和 top league
df_hot = df.dropna(subset=['league_hot_row_num'])
df_top = df_hot[df_hot['league_id'].isin(topLeague_list)]
# 排序
df_hot = df_hot.sort_values(by='league_hot_row_num')
df_top = df_top.sort_values(by='league_hot_row_num')
# 获取字典
hot_data = df_hot.to_dict(orient='records')
top_data = df_top.to_dict(orient='records')
hot_league = create_data(hot_data)
top_league = create_data(top_data)

# 创建yaml文件
save_hot = 'yaml/hotleague.yaml'
save_top = 'yaml/topleague.yaml'
with open(save_hot, 'w', encoding='utf-8') as f:
    yaml.dump(hot_league, f, 
    allow_unicode=True,  # 支持中文
    default_flow_style=False,  # 使用块状格式
    sort_keys=False,  # 不对键进行排序
    indent=2)  # 设置缩进为2个字符
with open(save_top, 'w', encoding='utf-8') as f:
    yaml.dump(top_league, f, 
    allow_unicode=True,  # 支持中文
    default_flow_style=False,  # 使用块状格式
    sort_keys=False,  # 不对键进行排序
    indent=2)  # 设置缩进为2个字符