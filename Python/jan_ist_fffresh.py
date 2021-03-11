import pandas as pd
from data_storage import connection
import xlrd

df = pd.read_excel("./manual_extracted_sec_files.xlsx", usecols=[
                   "NameOfCompany", "Class", "CUSIP", "MarketValue","SharesHeld", "date"]
                   , dtype= {"CUSIP": str})
#print(df.max())
#print(df.dtypes)
df.to_sql(
    "let_me_investigate", connection, if_exists="replace", index=False)