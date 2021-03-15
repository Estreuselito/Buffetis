import pandas as pd
from data_storage import connection
from financial_ratios import compute_financial_ratios, add_prev_years
import numpy as np
from find_neighbours import find_neighbour
from logger import logger
import math

logger.info("Loading the stocks data from local drive!\n")
stocks_buffett = pd.read_sql('Select date, cusip, return from stocks_m', connection)

stocks_buffett["cusip"] = stocks_buffett["cusip"].astype(str).str[:8]
stocks_buffett['year'] = stocks_buffett['datadate'].dt.year
stocks_buffett['month'] = stocks_buffett['datadate'].dt.month

stocks_buffett.to_sql('stock_match_mth', connection,
                      if_exists="replace", index=False)

logger.info("Reading the cleaned SEC data from the SQL Database!\n")

sec_filings = pd.read_sql(
    'SELECT SUBSTR(CUSIP, 1, 8) as cusip, MIN(date) AS date FROM Clean_SEC_filings csf GROUP BY CUSIP', connection, parse_dates=["date"])

sec_filings['year'] = sec_filings['date'].dt.year
sec_filings['month'] = sec_filings['date'].dt.month

sec_filings.to_sql('sec_filings_mth', connection, if_exists="replace", index=False)

logger.info("Reading the merge dataframe, which will next be enriched with all the data!\n")

final_df = pd.read_sql("select *, b.cusip as cusip2 from stock_match_mth a left join sec_filings_mth b on a.cusip = b.cusip and a.year = b.year", connection)

final_df = final_df.loc[:, ~final_df.columns.duplicated()]
final_df = compute_financial_ratios(final_df)

# Find index of first financial ratio, which we calculated
index_metrics = final_df.columns.get_loc('Gross_Profit_Margin')
# Retrieve column names of all financial ratios
metrics = final_df.columns[index_metrics:]
final_df = add_prev_years(final_df, 10, list(metrics))

# find neighbours
neighbours = find_neighbour(final_df, sec_filings)

dummy = [1 if x is not None else 0 for x in final_df['cusip2']]

final_df['cusip2'] = dummy
final_df = final_df.rename(columns={'cusip2': 'dummy_variable'})
final_df = final_df.merge(neighbours, on=["cusip", "fyear"], how="left")
# final_df["dummy_variable_x"].value_counts()
# final_df["dummy_variable_y"].fillna(0).value_counts()
final_df["dummy_variable"] = final_df["dummy_variable_x"] + \
    final_df["dummy_variable_y"].fillna(0)
final_df = final_df[final_df["dummy_variable"] != 0]
final_df = final_df[final_df["dummy_variable"] != 3]

# final_df = final_df.dropna(subset=["dummy_variable"])
final_df = final_df.replace([np.inf, -np.inf], np.nan)
final_df["dummy_variable"] = final_df["dummy_variable"].replace(2, 0)
final_df.to_sql('monthly_match', connection, if_exists="replace")
logger.info("Done!\n")
