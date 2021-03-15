# This file will download, import and digest the data
# into the database.
import pandas as pd
from data_storage import connection
from receiving_sec_data import SEC
import wrds
from get_cusips import Cusips
from logger import logger

# General usage
wrds_conn = wrds.Connection()
# Yanniks usage
logger.info("\nPlease input your Wharton Username and Password\n")
# wrds_conn = wrds.Connection(wrds_username="gacela")

# # # the following line of code, receivces all data from the SEC file server
logger.info("\nReceiving the data from the SEC filings.\n")


manuel_extracted_years = pd.read_excel("./SEC_filings_final.xlsx", dtype={"CUSIP_8Digits": str, "Date": str, "CUSIP_9Digits": str})

manuel_extracted_years.to_sql(
    "Quarterly_investments", connection, if_exists="replace", index=False)

# This is accessing and downlaoding the correct stock data of Wharton on a monthly basis
# Currently we want to get all stock informations of S&P 500 companies plus
# Warren Buffets investments
logger.info("\nReceiving the data from Wharton!\n")

ticker = Cusips(connection)
# total_cusips = ticker.get_all_cgusips()

logger.info("\nBe aware that currently the Stock data is limited to 100 rows!\nOnce you \
disable that limit it takes more than 20 min to receive all the data!\n")

wrds_conn.raw_sql(f"""SELECT
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
                      LEFT JOIN 
                      (select * from crsp.mse c where c.date >='01/01/1980' and c.comnam is not null) b 
                      ON a.cusip = b.cusip AND a.permno = b.permno
                      WHERE a.date>='01/01/1980'
                      AND a.cusip IN {ticker.get_all_cusips(8)}
                      AND b.cusip IN {ticker.get_all_cusips(8)}
                      """  # This can be deleted once this project is finished,
                  # however bear in mind, that if you delete the limit it can take
                  # quite a while to get all that data, I am talking here about
                  # 20 minutes!
                  ).to_sql("stocks_m", connection, if_exists="replace", index=False)

# This is accessing and downloading the anual fundamental data of Wharton for
# all S&P 500 companies plus Warren Buffets investments based on a ticker filter
wrds_conn.raw_sql(f"""SELECT
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
                      AND a.cusip IN {ticker.get_all_cusips(9)}"""
                  ).to_sql("fundamentals_a", connection,
                           if_exists="replace", index=False)

# this is accessing and downloading the quarterly fundamental data of Wharton for
# all S&P 500 companies plus Warren Buffets investments based on a ticker filter
#
wrds_conn.raw_sql(f"""SELECT
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
                      AND b.cusip IN {ticker.get_all_cusips(9)}"""
                  ).to_sql("fundamentals_q", connection,
                           if_exists="replace", index=False)

# Once we do not need the database anymore, we can close it
wrds_conn.close()
