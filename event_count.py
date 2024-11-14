import pandas as pd
from datetime import datetime, timedelta

# 导入 hub88_api 模块
import hub88_api as hub88

df = pd.read_json(r'pwd.json')

clientId = df['clientId'][0]  # 获取第一行的username
password = df['password'][0]  # 获取第一行的password

print(clientId, password)

token = hub88.get_token(clientId, password)

startDate_list = ["2024-11-13","2024-11-14","2024-11-15","2024-11-16",  "2024-11-17", "2024-11-18", "2024-11-19"]
start_date = datetime(2023, 11, 14)
end_date = datetime(2024, 11, 14)
date_list = []
current_date = start_date
while current_date <= end_date:
    date_list.append(current_date.strftime('%Y-%m-%d'))
    current_date += timedelta(days=1)
sportIds = [457]
# locationIds = [44,66,25,22,23,1,59]
schedule = []
for startDate in date_list:
    try:
      data = hub88.get_schedule_nolimit_location(token, startDate, sportIds)
      schedule.append({"startDate": startDate, "data_count": len(data)})
    except:
      schedule.append({"startDate": startDate, "data_count": 0})
    print(startDate)
    # schedule = schedule + data
    # break
df_schedule = pd.DataFrame(schedule)
save_path = r'data_count.csv'
df_schedule.to_csv(save_path, index=False)