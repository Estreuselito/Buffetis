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
# SEC.get_index(1993)
# SEC.save_to_database()

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

manuel_extracted_years = pd.read_excel("./manual_extracted_sec_files.xlsx", usecols=[
    "NameOfCompany", "Class", "CUSIP", "MarketValue", "SharesHeld", "date"], dtype={"CUSIP": str})

manuel_extracted_years.to_sql(
    "Quarterly_investments", connection, if_exists="append", index=False)

# Append to that table
from_2014.to_sql("Quarterly_investments",
                 connection, if_exists="append", index=False)

SEC.clean_SEC_filings()

# This is accessing and downlaoding the correct stock data of Wharton on a monthly basis
# Currently we want to get all stock informations of S&P 500 companies plus
# Warren Buffets investments
ticker = Cusips(connection)
total_cusips = ticker.get_all_cusips()

stocks_m = wrds_conn.raw_sql(f"""SELECT 
                            a.permno AS permno,
                            a.cusip AS cusip , 
                            a.date AS date, 
                            b.comnam AS company_name,
                            a.prc AS price, 
                            a.vol AS volume, 
                            a.ret AS return, 
                            a.retx AS return_ex, 
                            a.shrout AS shares_outstanding
                            FROM crsp.msf a
                            JOIN crsp.mse b ON b.cusip = a.cusip AND a.permno = b.permno
                            WHERE a.date>='01/01/1980'
                            AND a.cusip IN {total_cusips}"""
                             )

stocks_m.to_sql("stocks_m", connection, if_exists="replace", index=False)

# This is accessing and downloading the anual fundamental data of Wharton for
# all S&P 500 companies plus Warren Buffets investments based on a ticker filter
fundamentals_a = wrds_conn.raw_sql(f"""SELECT 
                                  a.tic AS ticker, 
                                  a.cusip AS cusip, 
                                  a.conm AS company_name,
                                  a.fdate AS date_a,
                                  a.gp AS gross_profit,
                                  a.revt AS revenue_total,
                                  a.xsga AS sga,
                                  a.xrd AS r_and_d,
                                  a.dp AS depr_amort,
                                  a.xint AS interest_expenses,
                                  a.ebit AS ebit,
                                  a.ni AS net_income,
                                  a.epsfx AS earnings_per_share_diluted,
                                  a.epspx AS earnings_per_share_basic,
                                  a.dt AS total_debt,
                                  a.teq AS stockholders_equity_total,
                                  a.dltt AS long_term_debt,
                                  a.oancf AS operating_net_cash_flow,
                                  a.seq AS stockholders_equity_total_gaap,
                                  a.at AS assets_total,
                                  a.lct AS current_liabilities_total,
                                  a.ppent AS total_ppe,
                                  a.act AS current_assets_total,
                                  a.dlc AS debt_current_liab,
                                  a.capx AS capital_expenditures,
                                  a.prstkc AS purchase_pref_common_stock,
                                  a.dv AS cash_dividends,
                                  a.dltis AS long_term_debt_issuance,
                                  a.dltr AS long_term_debt_reduction
                                  FROM comp.funda a
                                  WHERE a.fdate >='01/01/1980' 
                                  AND a.cusip IN {total_cusips}"""
                                   )

fundamentals_a.to_sql("fundamentals_a", connection,
                      if_exists="replace", index=False)

# this is accessing and downloading the quarterly fundamental data of Wharton for
# all S&P 500 companies plus Warren Buffets investments based on a ticker filter
#
fundamentals_q = wrds_conn.raw_sql(f"""SELECT 
                                   b.tic AS ticker, 
                                   b.cusip AS cusip, 
                                   b.conm AS company_name,
                                   b.fdateq AS date_q,
                                   b.xsgaq AS sga_q,
                                   b.revtq AS revenue_q,
                                   b.xrdq AS r_and_d_q,
                                   b.dpq AS depr_amort_q,
                                   b.xintq AS interest_expenses_q,
                                   b.dlttq AS long_term_debt_q,
                                   b.niq AS net_income_q,
                                   b.reunaq AS unadj_retained_earnings_q,
                                   b.req AS retained_earnings_q,
                                   b.tstkq AS treasury_stock_total_q
                                   FROM comp.fundq b
                                   WHERE b.fdateq >= '01/01/1980' 
                                   AND b.cusip IN {total_cusips}"""
                                   )

fundamentals_q.to_sql("fundamentals_q", connection,
                      if_exists="replace", index=False)


# Once we do not need the database anymore, we can close it
wrds_conn.close()
