# This file will download, import and digest the data
# into the database.
import pandas as pd
from data_storage import connection
import wrds
import os

wrds_conn = wrds.Connection()

#libraries = 
stocks = wrds_conn.get_table(library='crsp', 
                              table='msf', 
                              columns=['permno', 'date', 'prc', 'vol', 'ret', 'shrout'],
                              obs=5)

matchmaker = wrds_conn.get_table(library='crsp',
                                table = 'mse',
                                columns = ['comnam', 'permno', 'ticker'],
                                obs=5)

fundamentals = wrds_conn.get_table(library='comp',
                                   table = 'funda',
                                   columns = ['lo'],
                                   obs=5)

ticker = pd.read_csv('./Data/Ticker_symbols.csv', sep=';')
ticker = list(ticker.columns)




