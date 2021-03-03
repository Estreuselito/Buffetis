# This file will download, import and digest the data
# into the database.
import pandas as pd
from data_storage import connection
from receiving_sec_data import SEC

# the following line of code, receivces all data from the SEC file server
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
