import statsmodels.api as sm
import pandas as pd
from data_storage import connection
from logger import logger
import numpy as np

monthly_match = pd.read_sql("""SELECT Gross_Profit_Margin_t0,
                                      Gross_Profit_Margin_avg,
                                      Net_Profit_Margin_t0,
                                      Net_Profit_Margin_avg,
                                      dummy_variable
                             FROM monthly_match""", connection)
monthly_match.isnull().sum()
monthly_match["dummy_variable"].value_counts()
# monthly_match = monthly_match.dropna()
monthly_match.isnull().sum()
monthly_match = monthly_match.replace([np.inf, -np.inf], np.nan)
result = sm.Probit(
    monthly_match["dummy_variable"], monthly_match.loc[:, monthly_match.columns != 'dummy_variable'], missing="drop").fit()
print(result.summary())
