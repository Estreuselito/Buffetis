import pandas as pd 
from data_storage import connection

# this small cute script calculates the average return per quarter fopr the whole stock market
#from 1995 to 2020 and outputs it in a csv
benchmark_stocks_9509 = pd.read_sql('select date, quarters, avg(ret) as average_return from stocks_all_9509 group by date, quarters', connection)
benchmark_stocks_1020 = pd.read_sql('select date, quarters, avg(ret) as average_return from stocks_all_1020 group by date, quarters', connection)

df_list = [benchmark_stocks_9509, benchmark_stocks_1020]
benchmark_stock9520 = pd.concat(df_list)

benchmark_stock9520.to_csv('benchmark_stock9520.csv')