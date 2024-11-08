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
# print(df_enzh)

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
  'Bangalore'
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
  'Salvador',
  'Fortaleza',
  'Belo Horizonte',
  'Manaus',
  'Curitiba',
  'Recife',
  'Porto Alegre',
  'Belém',
  'Goiânia',
  'Guarulhos',
  'Campinas',
  'São Luís',
  'São Gonçalo',
  'Maceió',
  'Duque de Caxias',
  'Natal',
  'Teresina',
  'Nova Iguaçu',
  'Campo Grande',
  'João Pessoa',
  'São Bernardo do Campo',
  'Santo André',
  'Osasco',
  'Aracaju',
  'Jaboatão dos Guararapes',
  'Ribeirão Preto',
  'Uberlândia',
  'Acre',  
  'Alagoas',
  'Amapá',
  'Amazonas',
  'Bahia',
  'Ceará',
  'Distrito Federal',
  'Espírito Santo',
  'Goiás',
  'Maranhão',
  'Mato Grosso',
  'Mato Grosso do Sul',
  'Minas Gerais',
  'Pará',
  'Paraíba',
  'Paraná',
  'Pernambuco',
  'Piauí',
  'Rio de Janeiro',
  'Rio Grande do Norte',
  'Rio Grande do Sul',
  'Rondônia',
  'Roraima',
  'Santa Catarina',
  'São Paulo',
  'Sergipe',
  'Tocantins',
  'div 3',
  'div 4',
  'div 2',
  '2 div',
  '3 div',
  '4 div',
  'division 2',
  'division 3',
  'division 4',
  'division three',
  'division four',
  'division two',
  '2 division',
  '3 division',
  '4 division',
  'Algeria',  
'Angola',  
'Benin',  
'Botswana',  
'Burkina Faso',  
'Burundi',  
'Cabo Verde',  
'Cameroon',  
'Central African Republic',  
'Chad',  
'Comoros',  
'Democratic Republic of the Congo',  
'Republic of the Congo',  
'Djibouti',  
'Egypt',  
'Equatorial Guinea',  
'Eritrea',  
'Eswatini',  
'Ethiopia',  
'Gabon',  
'Gambia',  
'Ghana',  
'Guinea',  
'Guinea-Bissau',  
'Ivory Coast',  
'Kenya',  
'Lesotho',  
'Liberia',  
'Libya',  
'Madagascar',  
'Malawi',  
'Mali',  
'Mauritania',  
'Mauritius',  
'Morocco',  
'Mozambique',  
'Namibia',  
'Niger',  
'Nigeria',  
'Rwanda',  
'Sao Tome and Principe',  
'Senegal',  
'Seychelles',  
'Sierra Leone',  
'Somalia',  
'South Africa',  
'South Sudan',  
'Sudan',  
'Tanzania',  
'Togo',  
'Tunisia',  
'Uganda',  
'Zambia',  
'Zimbabwe',
'阿尔及利亚',  
'安哥拉',  
'贝宁',  
'博茨瓦纳',  
'布基纳法索',  
'布隆迪',  
'佛得角',  
'喀麦隆',  
'中非共和国',  
'乍得',  
'科摩罗',  
'刚果',   
'吉布提',  
'埃及',  
'赤道几内亚',  
'厄立特里亚',  
'斯威士兰',  
'埃塞俄比亚',  
'加蓬',  
'冈比亚',  
'加纳',  
'几内亚',  
'几内亚比绍',  
'科特迪瓦',  
'肯尼亚',  
'莱索托',  
'利比里亚',  
'利比亚',  
'马达加斯加',  
'马拉维',  
'马里',  
'毛里塔尼亚',  
'毛里求斯',  
'摩洛哥',  
'莫桑比克',  
'纳米比亚',  
'尼日尔',  
'尼日利亚',  
'卢旺达',  
'圣多美和普林西比',  
'塞内加尔',  
'塞舌尔',  
'塞拉利昂',  
'索马里',  
'南非',  
'南苏丹',  
'苏丹',  
'坦桑尼亚',  
'多哥',  
'突尼斯',  
'乌干达',  
'赞比亚',  
'津巴布韦',
'低级',
'中级',
'高级',
'初级',
'业余',
'上级',
'下级',
'青年',
'乌克兰',
'ukraine',
'Reserves',
'预备',
]

# 创建一个布尔索引，检查每行的 'league-en' 列是否包含列表中的任意一个字符串片段
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
region_na_en_count = sport_is_na_en.sum()

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

# 将匹配的行保存到 CSV 文件
# matched_rows.to_csv('matched_rows.csv', index=False, encoding='utf-8')