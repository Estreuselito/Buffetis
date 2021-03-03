import pandas as pd
from data_storage import connection


#imports the data
df_a = pd.read_sql_query('''SELECT * FROM fundamentals_a''', connection)

df_q =  pd.read_sql_query('''SELECT * FROM fundamentals_q''', connection)


def calc_gross_profit_margin(gross_profit, revenue):

    gross_profit_margin = gross_profit/ revenue

    return gross_profit_margin


def calc_sga_expense_ratio(sga, revenue):

    sga_expense_ratio = sga / revenue
    
    return sga_expense_ratio


def calc_rnd_expense_ratio(rnd, revenue):

    rnd_expense_ratio = rnd / revenue

    return rnd_expense_ratio


def calc_depreciation_expense_ratio(depreciation, revenue):

    depreciation_expense_ratio = depreciation / revenue

    return depreciation_expense_ratio


def calc_interest_expense_ratio(interest, revenue):

    interest_expense_ratio = interest / revenue

    return interest_expense_ratio


def calc_net_profit_margin(net_income, revenue):

    net_profit_margin = net_income / revenue

    return net_profit_margin


def calc_earnings_per_share():

    return 0


def calc_debt_to_eq_ratio(debt, equity):

    debt_to_eq_ratio = debt / equity

    return debt_to_eq_ratio


def calc_lt_debt_ratio(lt_debt, net_income):

    lt_debt_ratio = lt_debt / net_income

    return lt_debt_ratio


def calc_cf_coverage_ratio(op_cf, total_debt):

    cf_coverage_ratio = op_cf / total_debt

    return cf_coverage_ratio


def calc_return_on_equity(net_income, equity):

    return_on_equity = net_income / equity

    return return_on_equity


def calc_return_capital_employed(ebit, total_assets, current_liabilities):

    return_capital_employed = ebit / (total_assets - current_liabilities)
    
    return return_capital_employed


def calc_return_net_assets(net_income, fixed_assets, net_working_capital):

    return_net_assets = net_income / (fixed_assets + net_working_capital)

    return return_net_assets


def calc_capital_expenditure_ratio(capital_expenditure, revenue):

    capital_expenditure = capital_expenditure / revenue

    return capital_expenditure


def calc_company_repurchasing():

    return 0 


def calc_divident_netincome_ratio(divident_paid, net_income):

    divident_netincome_ratio = divident_paid / net_income

    return divident_netincome_ratio


def calc_fcfe(op_net_cash_flow, capital_expenditures):

    fcfe = 0

    return fcfe


def calc_market_timing(price, earnings_ratio):

    market_timing = 0

    return market_timing


#calculate all annual fundamental ratios

fundamental_ratios = {}

fundamental_ratios['cusip'] = df_a['cusip']
fundamental_ratios['company_name'] = df_a['company_name']
fundamental_ratios['gross_profit_margin'] = calc_gross_profit_margin(df_a['gross_profit'], df_a['revenue_total'])
fundamental_ratios['sga_expense_ratio'] = calc_sga_expense_ratio(df_a['sga'], df_a['revenue_total'])
fundamental_ratios['rnd_expense_ratio'] = calc_rnd_expense_ratio(df_a['r_and_d'], df_a['revenue_total'])
fundamental_ratios['depreciation_expense_ratio'] = calc_depreciation_expense_ratio(df_a['depr_amort'], df_a['revenue_total'])
fundamental_ratios['interest_expense_ratio'] = calc_interest_expense_ratio(df_a['interest_expenses'], df_a['revenue_total'])
fundamental_ratios['net_profit_margin'] = calc_net_profit_margin(df_a['net_income'], df_a['revenue_total'])
#calc_earnings_per_share()
fundamental_ratios['debt_to_eq_ratio'] = calc_debt_to_eq_ratio(df_a['total_debt'], df_a['stockholders_equity_total_gaap'])
fundamental_ratios['lt_debt_ratio'] = calc_lt_debt_ratio(df_a['long_term_debt'], df_a['net_income'])
fundamental_ratios['cf_coverage_ratio'] = calc_cf_coverage_ratio(df_a['operating_net_cash_flow'], df_a['total_debt'])
fundamental_ratios['return_on_equity'] = calc_return_on_equity(df_a['net_income'], df_a['stockholders_equity_total_gaap'])
fundamental_ratios['return_capital_employed'] = calc_return_capital_employed(df_a['ebit'], df_a['assets_total'], df_a['current_liabilities_total'])
#return_net_assets = calc_return_net_assets(df_a['net_income'], df_a['current_assets_total'], net_working_capital)
fundamental_ratios['capital_expenditures_ratio'] = calc_capital_expenditure_ratio(df_a['capital_expenditures'], df_a['revenue_total'])
#calc_company_repurchasing()
fundamental_ratios['divident_net_income_ratio'] = calc_divident_netincome_ratio(df_a['cash_dividends'], df_a['net_income'])
#calc_fcfe(op_net_cash_flow, capital_expenditures)
#calc_market_timing(price, earnings_ratio)

fundamental_ratios_annual = pd.DataFrame.from_dict(fundamental_ratios)

fundamental_ratios_annual.to_sql("fundamental_ratios_annual", connection, if_exists="replace", index=False)