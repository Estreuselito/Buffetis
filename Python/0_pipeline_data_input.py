# This file will download, import and digest the data
# into the database.
import pandas as pd
from data_storage import connection

berkshire = pd.read_csv("./data/berkshire_investments.csv",
                        skiprows=1, encoding="utf-8")

berkshire.to_sql("investments_buffet",
                 connection=connection,
                 if_exists="replace")
