import pandas as pd
from data_storage import connection
import wrds


class Cusips():

    def get_all_cusips(self, wrds_connection, sql_connection):
        wrds_conn = wrds_connection
        # get cusips from Warren Buffets investment
        cusips_yannik = pd.read_sql_query(
            "select distinct cusip from Quarterly_investments", sql_connection)
            
        cusips_dict_yannik = cusips_yannik.to_dict(orient='list')

        cusips_yannik = cusips_dict_yannik['CUSIP']

        # merge both cusip sources and filter the duplicates
        total_cusips = [x for x in cusips_yannik if x is not None]

        return tuple(total_cusips)
