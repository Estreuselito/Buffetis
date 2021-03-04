class Financial_ratios():
    def gross_profit_margin(self, gross_profit, revenue):

        gross_profit_margin = gross_profit / revenue
        return gross_profit_margin

    def sga_expense_ratio(self, sga, revenue):

        sga_expense_ratio = sga / revenue
        return sga_expense_ratio

    def rnd_expense_ratio(self, rnd, revenue):

        rnd_expense_ratio = rnd / revenue
        return rnd_expense_ratio

    def depreciation_expense_ratio(self, depreciation, revenue):

        depreciation_expense_ratio = depreciation / revenue
        return depreciation_expense_ratio

    def interest_expense_ratio(self, interest, revenue):

        interest_expense_ratio = interest / revenue
        return interest_expense_ratio

    def net_profit_margin(self, net_income, revenue):

        net_profit_margin = net_income / revenue
        return net_profit_margin

    def debt_to_eq_ratio(self, debt, equity):

        debt_to_eq_ratio = debt / equity
        return debt_to_eq_ratio

    def lt_debt_ratio(self, lt_debt, net_income):

        lt_debt_ratio = lt_debt / net_income
        return lt_debt_ratio

    def cf_coverage_ratio(self, op_cf, total_debt):

        cf_coverage_ratio = op_cf / total_debt
        return cf_coverage_ratio

    def return_on_equity(self, net_income, equity):

        return_on_equity = net_income / equity
        return return_on_equity

    def return_capital_employed(self, ebit, total_assets, current_liabilities):

        return_capital_employed = ebit / (total_assets - current_liabilities)
        return return_capital_employed

    def return_net_assets(self, net_income, fixed_assets, net_working_capital):

        return_net_assets = net_income / (fixed_assets + net_working_capital)
        return return_net_assets

    def capital_expenditure_ratio(self, capital_expenditure, revenue):

        capital_expenditure = capital_expenditure / revenue
        return capital_expenditure

    def earnings_per_share(self):

        return 0

    def company_repurchasing(self):

        return 0

    def divident_netincome_ratio(self, divident_paid, net_income):

        divident_netincome_ratio = divident_paid / net_income
        return divident_netincome_ratio

    def fcfe(self, op_net_cash_flow, capital_expenditures):

        fcfe = 0
        return fcfe

    def market_timing(self, price, earnings_ratio):

        market_timing = 0
        return market_timing
