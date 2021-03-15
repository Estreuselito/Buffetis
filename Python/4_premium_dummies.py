import pandas as pd
from data_storage import connection
import numpy as np
from logger import logger

df = pd.read_sql('Select * from buffett_premium', connection)

new_df = pd.DataFrame(columns = ['index', 'year', 'month', 'cusip', 'return', 'cusip2', 'dummy_variable', 'month_rank'])

CUSIP = df['cusip'].unique()

for i in CUSIP:
    data = df[df['cusip']== i]
    data.reset_index(drop=True)
    
    for j in range(len(data)):
        if data.iloc[j, -1] == 1:
            temp = j
            pass
        else:
            continue
    data['dummy_variable'] = 0
    data['month_rank'] = 0
    data_0 = data[:temp]
    data_1 = data[temp:]
    
    data_1['dummy_variable'] = 1
    data_0['dummy_variable'] = 0
    
    data_1['month_rank'] = np.arange(len(data_1))
    
    for z in range(len(data_0)):
        data_0.iloc[z, -1] = z-len(data_0) 
    
    new_df = new_df.append(data_0)
    new_df = new_df.append(data_1)

#new_df
new_df.to_csv(r'./data/premium_labeled.csv', index = False)