import pandas as pd
from data_storage import connection
import wrds


class Cusips():

    def get_all_cusips(self):
        #get cusips from Warren Buffets investment
        cusips_yannik = pd.read_sql_query("select distinct cusip from Quarterly_investments", connection)

        cusips_dict_yannik = cusips_yannik.to_dict(orient= 'list')

        cusips_yannik = cusips_dict_yannik['CUSIP']

        #merge both cusip sources and filter the duplicates
        total_cusips = [x for x in cusips_yannik if x is not None]

        return tuple(total_cusips)


    def get_all_ticker(self):

        ticker_jan = pd.read_sql_query("select distinct ticker from fundamentals_a", connection)

        tickers_dict_jan = ticker_jan.to_dict(orient= 'list')

        ticker_jan = tickers_dict_jan['ticker']

        return tuple(ticker_jan)
