import sqlite3
import pandas as pd
conn = sqlite3.connect('data/fintech_sandbox.db')
df_users = pd.read_sql('select * from users', conn)
total = len(df_users)
df_transactions = pd.read_sql('select * from transactions', conn)
df_megred = pd.merge(df_users, df_transactions, on='user_id', how='left')
is_empty = df_megred['tx_id'].isna()
df_inactive = df_megred[is_empty]
inactive = len(df_inactive)
active = total - inactive 
conversation = (active/total)*100
print(conversation)