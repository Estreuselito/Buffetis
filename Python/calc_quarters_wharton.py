import pandas as pd
from data_storage import connection

#creates a space separeted string
def convert(lst): 
      
    return ' '.join(lst)


def i_want_cusips_fast():
    yannik_cusip = pd.read_sql_query('''SELECT distinct CUSIP FROM Quarterly_investments''', connection)
    yannik_cusip_list = yannik_cusip['CUSIP']
    yannik_cusip_liste = [x for x in yannik_cusip_list if x is not None]

    return convert(yannik_cusip_listen)

space_seperated_list = i_want_cusips_fast(yannik_cusip_listen)
#I printed this list and copied it into Wharton Cloud to retrieve all the needed data


#I had to split the stocks_all to stocks_all_9509 and stocks_all1020
#so its possible to bring them into a dataframe
#both files together have approx. 3 million rows
stocks_buffett = pd.read_csv('./data/stocks_buffett.csv', sep=',')
stocks_all_9509 = pd.read_csv('./data/stocks_all_9509.csv', sep=',')
stocks_all_1020 = pd.read_csv('./data/stocks_all_1020.csv', sep=',')


#this slice the date so its only the year and the month for each row
stocks_all_1020['date'] = stocks_all_1020['date'].astype(str).str[:6]
stocks_all_9509['date'] = stocks_all_9509['date'].astype(str).str[:6]
stocks_buffett['date'] = stocks_buffett['date'].astype(str).str[:6]



#calc quarters for all stock data from 1995 to 2009 including
quarter1 = [1 if x == '12' or x == '02' or x == '01' else 0 for x in stocks_all_9509["date"].str[-2:]]         
quarter2 = [2 if x == '04' or x == '05' or x == '03' else 0 for x in stocks_all_9509["date"].str[-2:]]  
quarter3 = [3 if x == '07' or x == '08' or x == '06' else 0 for x in stocks_all_9509["date"].str[-2:]]  
quarter4 = [4 if x == '10' or x == '11' or x == '09' else 0 for x in stocks_all_9509["date"].str[-2:]]  

quarters = zip(quarter1, quarter2, quarter3, quarter4)
final_quarters = [x + y + v + z for (v, x, y, z) in quarters]

empty_dict1 = {}
stocks_all_9509['quarters'] = final_quarters
stocks_all_9509.append(empty_dict1, ignore_index = True)
stocks_all_9509['date'] = stocks_all_9509['date'].astype(str).str[:4]
stocks_all_9509.to_sql("stocks_all_9509", connection, if_exists="replace", index=False)
quarters = []


#calc quarters for all stock data from 2010 until 2020
quarter13 = [1 if x == '12' or x == '02' or x == '01' else 0 for x in stocks_all_1020["date"].str[-2:]]         
quarter23 = [2 if x == '04' or x == '05' or x == '03' else 0 for x in stocks_all_1020["date"].str[-2:]]  
quarter33 = [3 if x == '07' or x == '08' or x == '06' else 0 for x in stocks_all_1020["date"].str[-2:]]  
quarter43 = [4 if x == '10' or x == '11' or x == '09' else 0 for x in stocks_all_1020["date"].str[-2:]]  

quarters = zip(quarter13, quarter23, quarter33, quarter43)
final_quarters = [x + y + v + z for (v, x, y, z) in quarters]

empty_dict1 = {}
stocks_all_1020['quarters'] = final_quarters
stocks_all_1020.append(empty_dict1, ignore_index = True)
stocks_all_1020['date'] = stocks_all_1020['date'].astype(str).str[:4]
stocks_all_1020.to_sql("stocks_all_1020", connection, if_exists="replace", index=False)


#calc quarter for all investments of warren buffet investes stocks
quarter11 = [1 if x == '12' or x == '02' or x == '01' else 0 for x in stocks_buffett["date"].str[-2:]]         
quarter21 = [2 if x == '04' or x == '05' or x == '03' else 0 for x in stocks_buffett["date"].str[-2:]]  
quarter31 = [3 if x == '07' or x == '08' or x == '06' else 0 for x in stocks_buffett["date"].str[-2:]]  
quarter41 = [4 if x == '10' or x == '11' or x == '09' else 0 for x in stocks_buffett["date"].str[-2:]]  

quarters2 = zip(quarter11, quarter21, quarter31, quarter41)
final_quarters2 = [x + y + v + z for (v, x, y, z) in quarters2]

empty_dict2 = {}
stocks_buffett['quarters'] = final_quarters2
stocks_buffett.append(empty_dict2, ignore_index = True)
stocks_buffett['date'] = stocks_buffett['date'].astype(str).str[:4]
stocks_buffett.to_sql("stocks_buffett", connection, if_exists="replace", index=False)

