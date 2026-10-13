import pandas as pd
accounts = pd.read_csv('data/accounts.csv')
print(accounts.head())
accounts['last_login'] = pd.to_datetime(accounts['last_login'])
accounts.info()
