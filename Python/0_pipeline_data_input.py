# This file will download, import and digest the data
# into the database.
import pandas as pd
from data_storage import connection

berkshire = pd.read_csv("./Data/berkshire_investments.csv",
                        delimiter=";",
                        encoding="utf-8",
                        index_col=[0])

berkshire.to_sql("warren_investments",
                 con=connection,
                 if_exists="replace")
