import pandas as pd
from data_storage import connection

(pd.read_sql("""SELECT CAST(CUSIP AS varchar) AS CUSIP,
                           CAST(MarketValue AS int) AS MarketValue,
                           CAST(SharesHeld as int) AS SharesHeld,
                           CAST(date AS varchar) AS date
                    FROM Quarterly_investments""",
             connection)
 .ffill()
 .groupby(by=["CUSIP", "date"])
 .sum()
 .reset_index()
 .to_sql("cleaned_dataframe1", connection, if_exists="replace", index=False))

# df = df.ffill()
# df = df.groupby(by=["CUSIP", "date"]).sum()
# df = df.reset_index()
# df.to_sql("cleaned_dataframe", connection, if_exists="replace", index=False)
