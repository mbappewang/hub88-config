import pandas as pd
# 映射关系
df = pd.read_csv('excel/映射表.CSV')
mapping = df.set_index('FB_id')['home_team_id'].to_dict()
print(mapping)

print(mapping.get(53210,None))