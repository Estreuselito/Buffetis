import pandas as pd
from data_storage import connection

Quarterly_investments = pd.read_sql('select * from Quarterly_investments', connection)


Quarterly_investments['date'] = Quarterly_investments['date'].astype(str).str[:7]
Quarterly_investments['date'] = Quarterly_investments['date'].astype(str).str[:7]


quarter1 = [1 if x == '01' or x == '02' or x == '03' else 0 for x in Quarterly_investments["date"].str[-2:]]         
quarter2 = [2 if x == '04' or x == '05' or x == '06' else 0 for x in Quarterly_investments["date"].str[-2:]]  
quarter3 = [3 if x == '07' or x == '08' or x == '09' else 0 for x in Quarterly_investments["date"].str[-2:]]  
quarter4 = [4 if x == '10' or x == '11' or x == '12' else 0 for x in Quarterly_investments["date"].str[-2:]]  
print(Quarterly_investments["date"].str[-2:])
quarters = zip(quarter1, quarter2, quarter3, quarter4)
final_quarters = [x + y + v + z for (v, x, y, z) in quarters]

empty_dict1 = {}
Quarterly_investments['quarters'] = final_quarters
Quarterly_investments.append(empty_dict1, ignore_index = True)
Quarterly_investments['CUSIP'] = Quarterly_investments['CUSIP'].astype(str).str[:8]
Quarterly_investments['date'] = Quarterly_investments['date'].astype(str).str[:4]
Quarterly_investments.to_sql("Quarterly_investments2", connection, if_exists="replace", index=False)

