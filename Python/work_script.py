import pandas as pd
from data_storage import connection

#yannik_cusip = pd.read_sql_query('''SELECT distinct CUSIP FROM Quarterly_investments''', connection)

#yannik_cusip_list = yannik_cusip['CUSIP']
#yannik_cusip_liste = [x for x in yannik_cusip_list if x is not None]
#yannik_cusip_listen = [x[:-1] for x in yannik_cusip_liste]

#converts yanniks cusips to space sperated string
def convert(lst): 
      
    return ' '.join(lst)

#space_seperated_list = convert(yannik_cusip_listen)


stocks_buffett = pd.read_csv('./data/stocks_buffett.csv', sep=',')
stocks_snp = pd.read_csv('./data/stocks_snp.csv', sep=',')

stocks_snp['date'] = stocks_snp['date'].astype(str).str[:6]
stocks_buffett['date'] = stocks_buffett['date'].astype(str).str[:6]


quarter1 = [1 if x == '01' or x == '02' or x == '03' else 0 for x in stocks_snp["date"].str[-2:]]         
quarter2 = [2 if x == '04' or x == '05' or x == '06' else 0 for x in stocks_snp["date"].str[-2:]]  
quarter3 = [3 if x == '07' or x == '08' or x == '09' else 0 for x in stocks_snp["date"].str[-2:]]  
quarter4 = [4 if x == '10' or x == '11' or x == '12' else 0 for x in stocks_snp["date"].str[-2:]]  

quarters = zip(quarter1, quarter2, quarter3, quarter4)
final_quarters = [x + y + v + z for (v, x, y, z) in quarters]

empty_dict1 = {}
stocks_snp['quarters'] = final_quarters
stocks_snp.append(empty_dict1, ignore_index = True)
stocks_snp['date'] = stocks_snp['date'].astype(str).str[:4]
stocks_snp.to_sql("stocks_snp", connection, if_exists="replace", index=False)



quarter11 = [1 if x == '01' or x == '02' or x == '03' else 0 for x in stocks_buffett["date"].str[-2:]]         
quarter21 = [2 if x == '04' or x == '05' or x == '06' else 0 for x in stocks_buffett["date"].str[-2:]]  
quarter31 = [3 if x == '07' or x == '08' or x == '09' else 0 for x in stocks_buffett["date"].str[-2:]]  
quarter41 = [4 if x == '10' or x == '11' or x == '12' else 0 for x in stocks_buffett["date"].str[-2:]]  

quarters2 = zip(quarter11, quarter21, quarter31, quarter41)
final_quarters2 = [x + y + v + z for (v, x, y, z) in quarters2]

empty_dict2 = {}
stocks_buffett['quarters'] = final_quarters2
stocks_buffett.append(empty_dict2, ignore_index = True)
stocks_buffett['date'] = stocks_buffett['date'].astype(str).str[:4]
stocks_buffett.to_sql("stocks_buffett", connection, if_exists="replace", index=False)

