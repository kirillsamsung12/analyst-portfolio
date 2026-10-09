import sqlite3
import pandas as pd
conn=sqlite3.connect('data/fintech_sandbox.db')
df_users = pd.read_sql('select * from users', conn)
df_cards = pd.read_sql('select * from cards', conn)
df_merge = pd.merge(df_users, df_cards, on='user_id', how='left')
df_no_cards = df_merge[df_merge['card_id'].isna()]
total = len(df_users)
no_cards = len(df_no_cards)
active = total - no_cards
conversion = (active/total)*100
print(conversion)
