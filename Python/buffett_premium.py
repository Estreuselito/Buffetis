import pandas as pd 
from data_storage import connection

avg_ret_buffett = pd.read_sql('select date, cusip, avg(ret) as average_return, quarters from stocks_buffett group by cusip, date, quarters', connection)
avg_ret_snp = pd.read_sql('select date, cusip, avg(ret), quarters from stocks_snp group by cusip, date, quarters', connection)
buffett_sec = pd.read_sql('select date, cusip, quarters from Quarterly_investments2 group by cusip, date, quarters', connection)


avg_ret_buffett.to_sql("avg_ret_buffett", connection, if_exists="replace", index=False)
avg_ret_snp.to_sql("avg_ret_snp", connection, if_exists="replace", index=False)
buffett_sec.to_sql("buffett_sec", connection, if_exists="replace", index=False)


df = pd.read_sql('select a.date, a.cusip, a.quarters, average_return, b.date, b.cusip, b.quarters from avg_ret_buffett a left join buffett_sec b on a.date = b.date and a.cusip = b.cusip and a.quarters = b.quarters', connection)
df.to_csv('avg_returns_buffett.csv')