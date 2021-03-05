# This file will download, import and digest the data
# into the database.
import pandas as pd
from data_storage import connection
from receiving_sec_data import SEC
import wrds
from get_cusips import Cusips

# General usage
#wrds_conn = wrds.Connection()
# Yanniks usage
wrds_conn = wrds.Connection(wrds_username="gacela")

# # the following line of code, receivces all data from the SEC file server
SEC = SEC(connection, "BERKSHIRE HATHAWAY INC", "13F-HR")
SEC.get_index(1993)
SEC.save_to_database()

# Queries the urls from the database
urls = pd.read_sql("SELECT TextUrl, DateOfIssue FROM SEC_filing_index",
                   connection, parse_dates=['DateOfIssue']).query('DateOfIssue <= "2012-03-01"')
# Uses the urls to access the Edgar Archives and returns a dataframe with
# the necessary information
until_2012 = SEC.extract_info_13F_until2012(urls["TextUrl"])

# Queries the urls from the database
urls = pd.read_sql("SELECT TextUrl, DateOfIssue FROM SEC_filing_index",
                   connection, parse_dates=['DateOfIssue']).query('DateOfIssue >= "2013-08-01"')
# Uses the urls to access the Edgar Archives and returns a dataframe with
# the necessary information
from_2014 = SEC.extract_info_13F_from2014(urls["TextUrl"])

# Create a new table in the database
until_2012.to_sql("Quarterly_investments",
                  connection, if_exists="replace", index=False)
# Append to that table
from_2014.to_sql("Quarterly_investments",
                 connection, if_exists="append", index=False)

SEC.clean_SEC_filings()

# This is accessing and downlaoding the correct stock data of Wharton on a monthly basis
# Currently we want to get all stock informations of S&P 500 companies plus
# Warren Buffets investments
ticker = Cusips()
total_cusips = ticker.get_all_cusips(wrds_conn, connection)

# This is accessing and downloading the anual fundamental data of Wharton for
# all S&P 500 companies plus Warren Buffets investments based on a ticker filter
fundamentals_a = wrds_conn.raw_sql(f""" select 
                                  a.tic as ticker, 
                                  a.cusip as cusip, 
                                  a.conm as company_name,
                                  a.fdate as date_a,
                                  a.gp as gross_profit,
                                  a.revt as revenue_total,
                                  a.xsga as sga,
                                  a.xrd as r_and_d,
                                  a.dp as depr_amort,
                                  a.xint as interest_expenses,
                                  a.ebit as ebit,
                                  a.ni as net_income,
                                  a.epsfx as earnings_per_share_diluted,
                                  a.epspx as earnings_per_share_basic,
                                  a.dt as total_debt,
                                  a.teq as stockholders_equity_total,
                                  a.dltt as long_term_debt,
                                  a.oancf as operating_net_cash_flow,
                                  a.seq as stockholders_equity_total_gaap,
                                  a.at as assets_total,
                                  a.lct as current_liabilities_total,
                                  a.ppent as total_ppe,
                                  a.act as current_assets_total,
                                  a.dlc as debt_current_liab,
                                  a.capx as capital_expenditures,
                                  a.prstkc as purchase_pref_common_stock,
                                  a.dv as cash_dividends,
                                  a.dltis as long_term_debt_issuance,
                                  a.dltr as long_term_debt_reduction
                                  from comp.funda a
                                  where a.fdate >='01/01/1980' 
                                  and a.cusip in {total_cusips}"""
                                   )

fundamentals_a.to_sql("fundamentals_a", connection,
                      if_exists="replace", index=False)

# this is accessing and downloading the quarterly fundamental data of Wharton for
# all S&P 500 companies plus Warren Buffets investments based on a ticker filter
#
fundamentals_q = wrds_conn.raw_sql(f""" select 
                                   b.tic as ticker, 
                                   b.cusip as cusip, 
                                   b.conm as company_name,
                                   b.fdateq as date_q,
                                   b.xsgaq as sga_q,
                                   b.revtq as revenue_q,
                                   b.xrdq as r_and_d_q,
                                   b.dpq as depr_amort_q,
                                   b.xintq as interest_expenses_q,
                                   b.dlttq as long_term_debt_q,
                                   b.niq as net_income_q,
                                   b.reunaq as unadj_retained_earnings_q,
                                   b.req as retained_earnings_q,
                                   b.tstkq as treasury_stock_total_q
                                   from comp.fundq b
                                   where b.fdateq >= '01/01/1980' 
                                   and b.cusip in {total_cusips}"""
                                   )

fundamentals_q.to_sql("fundamentals_q", connection,
                      if_exists="replace", index=False)

total_ticker = ticker.get_all_ticker()

stocks_m = wrds_conn.raw_sql(f"""select 
                            a.permno as permno,
                            a.cusip as cusip , 
                            a.date as date,
                            b.comnam as company_name, 
                            a.prc as price, 
                            a.vol as volume, 
                            a.ret as return, 
                            a.retx as return_ex, 
                            a.shrout as shares_outstanding
                            from crsp.msf a
                            join crsp.mse b on a.cusip = b.cusip and a.permno = b.permno
                            where a.date>='01/01/1980'
                            and b.ticker in {total_ticker}"""
                             )

stocks_m.to_sql("stocks_m", connection, if_exists="replace", index=False)


# Once we do not need the database anymore, we can close it
wrds_conn.close()
