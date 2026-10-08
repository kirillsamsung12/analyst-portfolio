import sqlite3
import pandas as pd

conn = sqlite3.connect("data/fintech_sandbox.db")
df_users = pd.read_sql("SELECT * FROM users", conn)

