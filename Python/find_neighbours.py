import pandas as pd
import numpy as np
from tqdm import tqdm


def find_neighbour(df_all, df_investments):

    # Count number of comparable investments
    count_investments = len(df_investments)

    # Initialize empty DataFrame for benchmark companies
    df_benchmark = pd.DataFrame()
    df_all = df_all.dropna(
        subset=["Depreciation_Expense_Ratio_t0", "Gross_Profit_Margin_t0", "Net_Profit_Margin_t0", "Long_Term_Debt_to_Net_Income_t0", "Fixed_Assets_to_Total_Assets_t0", "Dividend_Payout_Ratio_t0", "Rel_Change_Earnings_per_Share_t0"])

    for investment in tqdm(list(range(0, count_investments))):

        # Determine Cusip
        cusip = df_investments.loc[investment, "cusip"]
        # print(cusip)
        # Determine sic_code
        df_all["sic"] = df_all["sic"].astype(str).str[:2]
        # print(df_all["sic2"])
        # df_all["sic2"] = df_all["sic2"].astype(int)
        sic_code = df_all["sic"][df_all["cusip"] == cusip]
        # print(sic_code[:1])

        # Determine year
        year = df_investments.loc[investment, "year"]
        # print(sic_code)
        if len(sic_code) == 0:
            continue
        # Filter dataframe to only same industry
        # instead of sic_code, we need to only use the first two digits of the sic_code
        df_ind_match = df_all[df_all['sic'] == sic_code.values[0][:2]]

        # Filter dataframe to only same industry and year
        df_ind_year_match = df_ind_match[df_ind_match['fyear'] == year]

        if len(df_ind_year_match[df_ind_year_match['cusip'] == str(
                cusip)]['at']) == 0:
            continue
        # Find total assets of investment company by Warren Buffet
        total_assets_investment = df_ind_year_match[df_ind_year_match['cusip'] == str(
            cusip)]['at'].iloc[0]

        # Calculate Difference between assets total and append new column
        df_ind_year_match['dif_at'] = abs(
            df_ind_year_match.loc[:, 'at'] - total_assets_investment)

        # Sort Dataframe by difference
        df_ind_year_match_sorted = df_ind_year_match.sort_values('dif_at')
        # Second element will be the nearest neighbour (first element is investment company)
        if len(df_ind_year_match_sorted) > 1:
            benchmark = df_ind_year_match_sorted.iloc[1, :]
            df_benchmark = df_benchmark.append(benchmark)
        else:
            continue

    # Only return dataframe with cusip, sic and fyear
    df_benchmark = df_benchmark.loc[:, ['cusip', 'sic', 'fyear']]
    df_benchmark["dummy_variable"] = 2

    return df_benchmark
