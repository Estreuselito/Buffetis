# This file will download, import and digest the data
# into the database.
import pandas as pd
from data_storage import connection
import wrds

wrds_conn = wrds.Connection()

stocks = wrds_conn.get_table(library='crsp', 
                              table='msf', 
                              columns=['permno', 'date', 'prc', 'vol', 'ret', 'shrout'],
                              obs=5)

matchmaker = wrds_conn.get_table(library='crsp',
                                table = 'mse',
                                columns = ['comnam', 'permno', 'ticker'],
                                obs=5)


print(matchmaker)


