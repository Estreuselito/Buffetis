import pandas as pd
from data_storage import connection

df = pd.read_sql('select cusip, company_name from stocks_m', connection)


df = df.drop_duplicates()
df.to_csv('cusip2company_name.csv')