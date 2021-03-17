import pandas as pd
from data_storage import connection
import numpy as np
from logger import logger



logger.info("Loading the stocks data from local drive!\n")
stocks_buffett = pd.read_sql('Select date, cusip, return from stocks_m', connection)

stocks_buffett['year'] = stocks_buffett['date'].astype(str).str[:4]
stocks_buffett['month'] = stocks_buffett['date'].astype(str).str[5:7]

stocks_buffett.to_sql('stock_match_mth', connection,
                      if_exists="replace", index=False)

logger.info("Reading the cleaned SEC data from the SQL Database!\n")
sec_filings = pd.read_sql('SELECT CUSIP_8Digits as cusip, MIN(date) AS date FROM Quarterly_investments csf GROUP BY cusip', connection)
sec_filings['year'] = sec_filings['date'].astype(str).str[:4]
sec_filings['month'] = sec_filings['date'].astype(str).str[4:6]

sec_filings.to_sql('sec_filings_mth', connection, if_exists="replace", index=False)

logger.info("Reading the merge dataframe, which will next be enriched with all the data!\n")

final_df = pd.read_sql("select a.year, a.month, a.cusip, a.return, b.cusip as cusip2 from stock_match_mth a left join sec_filings_mth b on a.cusip = b.cusip and a.year = b.year and b.month = a.month", connection)

final_df = final_df.drop_duplicates()
dummy = [1 if x is not None else 0 for x in final_df['cusip2']]

final_df['cusip2'] = dummy 

#final_df.to_csv('premium_sheet.csv')
final_df.to_sql('buffett_premium', connection, if_exists="replace", index=False)