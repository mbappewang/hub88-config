import pandas as pd

# 假设 df_league, df_sport 和 df_region 已经被读取
df_league = pd.read_csv('leagues.csv')
df_sport = pd.read_csv('sports.csv')
df_region = pd.read_csv('regions.csv')

# 进行左连接
df_merged = df_league.merge(df_sport, how='left', left_on='sportId', right_on='id', suffixes=('_league', '_sport'))
df_merged = df_merged.merge(df_region, how='left', left_on='locationId', right_on='id', suffixes=('', '_region'))

# 打印合并后的 DataFrame
# print(df_merged)

# 将结果保存到 CSV 文件
# df_merged.to_csv('merged_league_sport_region.csv', index=False, encoding='utf-8')
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
  '甲',
  '乙',
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
]

# 创建一个布尔索引，检查每行的 'league-en' 列是否包含列表中的任意一个字符串片段
pattern = '|'.join(match_list)
contains_pattern_en = df_enzh['league-en'].str.contains(pattern, case=False, na=False)
contains_pattern_zh = df_enzh['league-zh'].str.contains(pattern, case=False, na=False)
is_na_en = df_enzh['league-en'].isna()

# 返回包含匹配字符串片段或 NaN 的行
matched_rows = df_enzh[contains_pattern_en | contains_pattern_zh | is_na_en]

# 打印匹配的行
print(matched_rows)

# 计算每个字符串匹配到的行数
match_counts = {pattern: ((df_enzh['league-en'].str.contains(pattern, case=False, na=False)) | 
                          (df_enzh['league-zh'].str.contains(pattern, case=False, na=False))).sum() 
                for pattern in match_list}

# 计算 NaN 匹配到的行数
na_en_count = is_na_en.sum()

# 打印每个字符串匹配到的行数
for pattern, count in match_counts.items():
    if count > 0:
      print(f"'{pattern}' matched {count} rows")

# 打印 NaN 匹配到的行数
print(f"'NaN in league-en' matched {na_en_count} rows")

# 将匹配的行保存到 CSV 文件
# matched_rows.to_csv('matched_rows.csv', index=False, encoding='utf-8')