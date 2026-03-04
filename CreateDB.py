import pandas as pd
import sqlite3

df = pd.read_csv("cleaned_customers.csv")
conn = sqlite3.connect("marketing.db")
df.to_sql("customers", conn, if_exists="append", index=False)
conn.close()