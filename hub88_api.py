import requests

def get_token(clientId,password):
  url = 'https://wintokens-dev-tradeart-api.trading.io/api/Account/login'
  payload = {'clientId': clientId, 'password': password}
  response = requests.post(url, json=payload)
  if response.status_code == 200:
    print("token获取成功")
    data = response.text
    return data
  else:
    print(f"获取Token失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code
  
def get_eventInfo(token, eventId):
  url = f'https://wintokens-dev-tradeart-api.trading.io/api/events/v2/{eventId}'
  headers = {'Authorization': f'Bearer {token}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print("请求eventInfo失败,状态码:", response.status_code)
    return response.status_code

def get_schedule(token,startDate,sportIds,locationIds):
  url = f'https://wintokens-dev-tradeart-api.trading.io/api/events/schedule/v2'
  headers = {'Authorization': f'Bearer {token}'}
  payload = {"startDate": startDate, 'sportIds': sportIds, 'locationIds': locationIds}
  response = requests.post(url, headers=headers, json=payload)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print(f"获取schedule失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code
  
def get_schedule_nolimit_location(token,startDate,sportIds):
  url = f'https://wintokens-dev-tradeart-api.trading.io/api/events/schedule/v2'
  headers = {'Authorization': f'Bearer {token}'}
  payload = {"startDate": startDate, 'sportIds': sportIds}
  response = requests.post(url, headers=headers, json=payload)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print(f"获取schedule失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code
  
def get_market_type(token,params,includeFreeText):
  url = f'https://wintokens-dev-tradeart-api.trading.io/api/schema/market-types?sportId={params}&includeFreeText={includeFreeText}'
  headers = {'Authorization': f'Bearer {token}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print(f"获取market_type失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code
  
def get_sports(token):
  url = 'https://wintokens-dev-tradeart-api.trading.io/api/schema/sports'
  headers = {'Authorization': f'Bearer {token}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print(f"获取sports失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code
  
def get_all_translation(token,Ids,module):
  url = f'https://wintokens-dev-tradeart-api.trading.io/api/translations/all/{module}/{Ids}'
  headers = {'Authorization': f'Bearer {token}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print(f"获取{module}translation失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code
  
def get_all_translation(token,Ids,module):
  url = f'https://wintokens-dev-tradeart-api.trading.io/api/translations/all/{module}/{Ids}'
  headers = {'Authorization': f'Bearer {token}'}
  response = requests.get(url, headers=headers)
  if response.status_code == 200:
    data = response.json()
    return data
  else:
    print(f"获取{module}translation失败,状态码: {response.status_code}")
    print("响应内容:", response.text)
    return response.status_code