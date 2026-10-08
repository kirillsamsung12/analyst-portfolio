# Тренировка с чистого листа
import sqlite3
import pandas as pd
conn = sqlite3.connect('data/fintech_sandbox.db')
df_users = pd.read_sql('SELECT * FROM transactions', conn) 
groups = df_users.groupby('category')
money = groups['amount']
result = money.sum()
print(result)