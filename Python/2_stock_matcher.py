import pandas as pd
from data_storage import connection
from financial_ratios import compute_financial_ratios, add_prev_years
import numpy as np
from find_neighbours import find_neighbour
from logger import logger
import math
# from scipy.stats.mstats import winsorize

logger.info("Loading the stocks data from local drive!\n")
# stocks_buffett = pd.read_csv(
#     './data/fundamentals_indl.csv', parse_dates=["datadate"])

# stocks_buffett["cusip"] = stocks_buffett["cusip"].astype(str).str[:8]
# stocks_buffett['year'] = stocks_buffett['datadate'].dt.year
# stocks_buffett['month'] = stocks_buffett['datadate'].dt.month

# stocks_buffett.to_sql('stock_match_mth', connection,
#                       if_exists="replace", index=False)

# logger.info("Reading the cleaned SEC data from the SQL Database!\n")
sec_filings = pd.read_sql(
    """SELECT CUSIP_8Digits as cusip, MIN(Date) AS date FROM Quarterly_investments WHERE CUSIP_8Digits IN
                (
                SELECT cusip FROM stock_match_mth
                )
        GROUP BY CUSIP_8Digits""", connection, parse_dates=["date"])
sec_filings['year'] = sec_filings['date'].dt.year
sec_filings['month'] = sec_filings['date'].dt.month

# sec_filings.to_sql('sec_filings_mth', connection,
#                    if_exists="replace", index=False)

logger.info(
    "Reading the merge dataframe, which will next be enriched with all the data!\n")
final_df = pd.read_sql(
    """select *, b.cusip as cusip2 from stock_match_mth a left join sec_filings_mth b on a.cusip = b.cusip and a.year = b.year""", connection)

final_df = final_df.loc[:, ~final_df.columns.duplicated()]
final_df = compute_financial_ratios(final_df)

# Find index of first financial ratio, which we calculated
index_metrics = final_df.columns.get_loc('Gross_Profit_Margin')
# Retrieve column names of all financial ratios
metrics = final_df.columns[index_metrics:]
final_df = add_prev_years(final_df, 10, list(metrics))

final_df = final_df.dropna(
    subset=["Return_on_Equity_t0", "Depreciation_Expense_Ratio_t0", "Gross_Profit_Margin_t0",
            "Rel_Change_Earnings_per_Share_t0", "Interest_Expense_Ratio_t0",
            "Net_Profit_Margin_t0", "D/E_Ratio_t0", "Fixed_Assets_to_Total_Assets_t0",
            "Return_on_Equity_avg", "Depreciation_Expense_Ratio_avg", "Gross_Profit_Margin_avg",
            "Rel_Change_Earnings_per_Share_avg", "Interest_Expense_Ratio_avg", "Net_Profit_Margin_avg",
            "D/E_Ratio_avg", "Fixed_Assets_to_Total_Assets_avg"]
    # ["Depreciation_Expense_Ratio_avg", "Gross_Profit_Margin_avg",
    #         "Rel_Change_Earnings_per_Share_avg", "Net_Profit_Margin_avg",
    #         "Return_on_Equity_avg", "D/E_Ratio_avg"]
)
final_df.loc[:, "sic"] = final_df.loc[:, "sic"].astype(str).str[:2]

# find neighbours
df_benchmark, blacklist, df_initial_invest = find_neighbour(
    final_df, sec_filings)

df_final_to_merge = df_benchmark.append(df_initial_invest)
df_final_to_merge = df_final_to_merge.merge(
    final_df, on=["cusip", "fyear"], how="left")
df_final_to_merge = df_final_to_merge.replace([np.inf, -np.inf], np.nan)
# cols = df_final_to_merge.select_dtypes(np.number).columns
# df_final_to_merge[cols] = df_final_to_merge[cols].clip(lower=df_final_to_merge[cols].quantile(
#     0.15), upper=df_final_to_merge[cols].quantile(0.85), axis=1)
df_final_to_merge.to_sql('monthly_match', connection,
                         if_exists="replace", index=False)
logger.info("Done!\n")
