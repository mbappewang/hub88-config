import pandas as pd

# 假设 df_league, df_sport 和 df_region 已经被读取
df_league = pd.read_csv('leagues.csv')
df_sport = pd.read_csv('sports.csv')
df_region = pd.read_csv('regions.csv')

# 进行左连接
df_merged = df_league.merge(df_sport, how='left', left_on='sportId', right_on='id', suffixes=('_league', '_sport'))
df_merged = df_merged.merge(df_region, how='left', left_on='locationId', right_on='id', suffixes=('', '_region'))
df_merged = df_merged[df_merged['sportId'].isin([457, 7, 1, 8, 14, 4, 11, 41, 20, 2, 23, 6, 48, 42, 25, 17, 5, 49, 28, 38, 39, 56, 57, 58, 60, 21, 12, 13, 160, 193, 589, 721, 27, 94, 33, 16, 15, 9, 59, 19, 22, 29, 34, 35, 54, 40, 18, 26, 51, 52, 53, 30, 37, 43, 45, 47, 61, 62, 63, 127, 1117, 886, 622, 1183, 1381])]

# 选择需要的列
df_enzh = df_merged[['id_league','league-en', 'league-zh', 'sportId','sport-en', 'sport-zh', 'locationId', 'region-en', 'region-zh']]
df_enzh.to_csv('merged_league_sport_region.csv', index=False, encoding='utf-8')
print(df_enzh)

# 假设要匹配的字符串列表
match_list = [
  'U10',
  'U11',
  'U12',
  'U13',
  'U14',
  'U15',
  'U16',
  'U17',
  'U18',
  'U19',
  'U20',
  'U21',
  'U22',
  'U23',
  '丙',
  '丁',
  '州',
  '省',
  '市',
  '县',
  '地区',
  '邦',
  '北部',
  '东部',
  '南部',
  '西部',
  '东北',
  '东南',
  '西南',
  '西北',
  '中部',
  '运',
  '缅甸',
  '香港',
  '台湾',
  'Mumbai',
  'Delhi',
  'Bangalore',
  'Hyderabad',
  'Ahmedabad',
  'Chennai',
  'Kolkata',
  'Pune',
  'Jaipur',
  'Surat',
  'Lucknow',
  'Kanpur',
  'Nagpur',
  'Visakhapatnam',
  'Indore',
  'Thane',
  'Bhopal',
  'Patna',
  'Vadodara',
  'Ghaziabad',
  'Ludhiana',
  'Agra',
  'Nashik',
  'Faridabad',
  'Meerut',
  'Rajkot',
  'Kalyan-Dombivli',
  'Vasai-Virar',
  'Varanasi',
  'Srinagar',
  'São Paulo',  
  'Rio',
  'Brasília',
  'Angola',
  '乌克兰',
  'ukraine',
  'Reserves',
  '预备',
  "serie c",
  "serie d",
  "3rd",
  "4th",
  "2nd"
]

# 去重
df_enzh = df_enzh.drop_duplicates()

# 创建一个布尔索引，检查每行的 'league-en' 和 'league-zh' 列是否包含列表中的任意一个字符串片段
pattern = '|'.join(match_list)
contains_pattern_en = df_enzh['league-en'].str.contains(pattern, case=False, na=False)
contains_pattern_zh = df_enzh['league-zh'].str.contains(pattern, case=False, na=False)
contains_pattern_region_en = df_enzh['region-en'].str.contains(pattern, case=False, na=False)
league_is_na_en = df_enzh['league-en'].isna()
sport_is_na_en = df_enzh['sport-en'].isna()
region_is_na_en = df_enzh['region-en'].isna()

# 返回包含匹配字符串片段或 NaN 的行
matched_rows = df_enzh[contains_pattern_en | contains_pattern_zh | league_is_na_en | sport_is_na_en | region_is_na_en | contains_pattern_region_en]

# 打印匹配的行
print(matched_rows)
print(df_enzh[['sport-en', 'sport-zh']].drop_duplicates().values.tolist())

# 计算每个字符串匹配到的行数
match_counts = {pattern: ((df_enzh['league-en'].str.contains(pattern, case=False, na=False)) | 
                          (df_enzh['league-zh'].str.contains(pattern, case=False, na=False)) |
                          (df_enzh['region-en'].str.contains(pattern,case=False,na=False))).sum() 
                for pattern in match_list}

# 计算 NaN 匹配到的行数
league_na_en_count = league_is_na_en.sum()
sport_na_en_count = sport_is_na_en.sum()
region_na_en_count = region_is_na_en.sum()

# 打印每个字符串匹配到的行数
for pattern, count in match_counts.items():
    if count > 0:
      print(f"'{pattern}' matched {count} rows")

# 打印 NaN 匹配到的行数
print(f"'NaN in league-en' matched {league_na_en_count} rows")
print(f"'NaN in sport-en' matched {sport_na_en_count} rows")
print(f"'NaN in region-en' matched {region_na_en_count} rows")

print(f"总黑名单行数{matched_rows.shape[0]}")
print(f"总白名单行数{df_enzh.shape[0]-matched_rows.shape[0]}")

# 打印没有被匹配到的行
unmatched_rows = df_enzh[~(contains_pattern_en | contains_pattern_zh | league_is_na_en)]
print(unmatched_rows)

# 将匹配的行保存到 CSV 文件
matched_rows.to_csv('matched_rows.csv', index=False, encoding='utf-8')

# 将未匹配的行保存到 CSV 文件
unmatched_rows.to_csv('unmatched_rows.csv', index=False, encoding='utf-8')

sportIds = list(set(unmatched_rows["sportId"].tolist()))
leagueIds = list(set(unmatched_rows["id_league"].tolist()))
white_list = [
   {"sportIds":sportIds},
    {"leagueIds":leagueIds}
]
import json
with open('hub88_process_whitelist.json', 'w') as f:
    json.dump(white_list, f, indent=2)