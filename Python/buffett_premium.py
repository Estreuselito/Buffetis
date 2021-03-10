import pandas as pd 
from data_storage import connection


#this script loads the stock data from Wharton and aggregates the average return of the quarter
avg_ret_buffett = pd.read_sql('select date, cusip, avg(ret) as average_return, quarters from stocks_buffett group by cusip, date, quarters', connection)

#this script loads the data of the SEC filings with the additional quarter column
buffett_sec = pd.read_sql('select date, cusip, quarters from Quarterly_investments2 group by cusip, date, quarters', connection)

#this loads the aggregated grouped to a table
avg_ret_buffett.to_sql("avg_ret_buffett", connection, if_exists="replace", index=False)
buffett_sec.to_sql("buffett_sec", connection, if_exists="replace", index=False)

#we left join the the grouped data of the SEC fillings to the stock data of Wharton 
#which should include exactly the same companies
#the idea behind it is, every time we have match it means that this quarter
#was the first in which Warren Buffett invested in this company
df = pd.read_sql('select a.date, a.cusip, a.quarters, average_return, b.date, b.cusip, b.quarters from avg_ret_buffett a left join buffett_sec b on a.date = b.date and a.cusip = b.cusip and a.quarters = b.quarters', connection)
df.to_csv('avg_returns_buffett.csv')