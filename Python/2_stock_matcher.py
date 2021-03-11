import pandas as pd
from data_storage import connection
import numpy as np

stocks_buffett = pd.read_csv('./data/stocks_buffett.csv')

stocks_buffett['year'] = stocks_buffett['date'].astype(str).str[:4]
stocks_buffett['month'] = stocks_buffett['date'].astype(str).str[4:6]

stocks_buffett.to_sql('stock_match_mth', connection, if_exists = "replace", index = False)


sec_filings = pd.read_sql('SELECT SUBSTR(CUSIP, 1, 8) as cusip, MIN(date) AS date FROM Clean_SEC_filings csf GROUP BY CUSIP', connection)
sec_filings['year'] = sec_filings['date'].str[:4]
sec_filings['month'] = sec_filings['date'].str[5:7]

sec_filings.to_sql('sec_filings_mth', connection, if_exists = "replace", index = False)


final_df = pd.read_sql("select a.cusip, a.year, a.month, a.ret as return, b.cusip as cusip2 from stock_match_mth a left join sec_filings_mth b on a.cusip = b.cusip and a.year = b.year and a.month = b.month", connection)

dummy = [1 if x is not None else np.nan for x in final_df['cusip2']]

final_df['cusip2'] = dummy
final_df = final_df.rename(columns={'cusip2': 'dummy_variable'})

final_df.to_csv('monthly_match.csv')