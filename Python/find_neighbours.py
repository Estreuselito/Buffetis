import pandas as pd
import numpy as np
from tqdm import tqdm


def find_neighbour(df_all, df_investments):
    # Here I create a blacklist, where all CUSIPS are saved which cannot be found in the df_all dataframe
    blacklist = []

    # Initialize empty DataFrame for benchmark companies
    df_benchmark = pd.DataFrame(columns=['cusip', 'sic', 'fyear'])
    df_initial_invest = pd.DataFrame(columns=['cusip', 'sic', 'fyear'])

    for index, cusip in tqdm(df_investments["cusip"].items()):
        # Find SIC from df_all for given CUSIP
        sic_code = df_all["sic"][df_all["cusip"] == cusip]
        # Check if SIC list is zero and if so input in blacklist
        if len(sic_code) == 0:
            blacklist.append(cusip)
            continue

        # Determine year
        year = df_investments.loc[index, "year"]

        # Filter dataframe to only same industry
        # instead of sic_code, we need to only use the first two digits of the sic_code
        df_ind_match = df_all.query(
            f"sic == '{sic_code.values[0][:2]}' and fyear == {year}")

        # Sanity check
        if len(df_ind_match['at'][df_ind_match['cusip'] == cusip]) == 0:
            blacklist.append(cusip)
            continue

        # Find total assets of investment company by Warren Buffet
        total_assets_investment = df_ind_match['at'][df_ind_match['cusip']
                                                     == cusip].iloc[0]

        # Calculate Difference between assets total and append new column
        df_ind_match.loc[:, 'dif_at'] = abs(
            df_ind_match.loc[:, 'at'] - total_assets_investment)

        # Sort Dataframe by difference
        df_ind_year_match_sorted = df_ind_match.sort_values(
            'dif_at').reset_index()

        if len(df_ind_year_match_sorted) > 1:
            benchmark = df_ind_year_match_sorted.iloc[1, :]
            df_benchmark = df_benchmark.append(benchmark)

            df_initial_invest = df_initial_invest.append(
                df_ind_year_match_sorted.iloc[0, :])
        else:
            blacklist.append(cusip)
            continue

    # Only return dataframe with cusip, sic and fyear
    df_benchmark = df_benchmark.loc[:, ['cusip', 'sic', 'fyear']].reset_index()
    df_benchmark["dummy_variable"] = 0

    df_initial_invest = df_initial_invest.loc[:, [
        'cusip', 'sic', 'fyear']].reset_index()
    df_initial_invest["dummy_variable"] = 1

    df_final_to_merge = df_benchmark.append(df_initial_invest)

    return df_benchmark, blacklist, df_initial_invest
