import pandas as pd
from data_storage import connection
from financial_ratios import Financial_ratios


# imports the data
df_a = pd.read_sql_query('''SELECT * FROM fundamentals_a''', connection)

df_q = pd.read_sql_query('''SELECT * FROM fundamentals_q''', connection)

Financial_metric = Financial_ratios()

# calculate all annual fundamental ratios an put them into a pandas DataFrame
fundamental_ratios_annual = pd.DataFrame.from_dict({
    "cusip": df_a['cusip'],
    "company_name": df_a['company_name'],
    "gross_profit_margin": Financial_metric.gross_profit_margin(df_a['gross_profit'], df_a['revenue_total']),
    "sga_expense_ratio": Financial_metric.sga_expense_ratio(df_a['sga'], df_a['revenue_total']),
    "rnd_expense_ratio": Financial_metric.rnd_expense_ratio(df_a['r_and_d'], df_a['revenue_total']),
    "depreciation_expense_ratio": Financial_metric.depreciation_expense_ratio(df_a['depr_amort'], df_a['revenue_total']),
    "interest_expense_ratio": Financial_metric.interest_expense_ratio(df_a['interest_expenses'], df_a['revenue_total']),
    "net_profit_margin": Financial_metric.net_profit_margin(df_a['net_income'], df_a['revenue_total']),
    "debt_to_eq_ratio": Financial_metric.debt_to_eq_ratio(df_a['total_debt'], df_a['stockholders_equity_total_gaap']),
    "lt_debt_ratio": Financial_metric.lt_debt_ratio(df_a['long_term_debt'], df_a['net_income']),
    "cf_coverage_ratio": Financial_metric.cf_coverage_ratio(df_a['operating_net_cash_flow'], df_a['total_debt']),
    "return_on_equity": Financial_metric.return_on_equity(df_a['net_income'], df_a['stockholders_equity_total_gaap']),
    "return_capital_employed": Financial_metric.return_capital_employed(df_a['ebit'], df_a['assets_total'], df_a['current_liabilities_total']),
    "capital_expenditures_ratio": Financial_metric.capital_expenditure_ratio(df_a['capital_expenditures'], df_a['revenue_total']),
    # "earnings_per_share": Financial_metric.earnings_per_share(),
    # "return_net_assets": Financial_metric.return_net_assets(df_a['net_income'], df_a['current_assets_total'], net_working_capital),
    # "company_repurchasing": Financial_metric.company_repurchasing(),
    "divident_net_income_ratio": Financial_metric.divident_netincome_ratio(df_a['cash_dividends'], df_a['net_income']),
    # "f_cash_f_to_eq": Financial_metric.fcfe(op_net_cash_flow, capital_expenditures),
    # "market_timing": Financial_metric.market_timing(price, earnings_ratio)
})

fundamental_ratios_annual.to_sql(
    "fundamental_ratios_annual", connection, if_exists="replace", index=False)
