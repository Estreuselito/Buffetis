class Financial_ratios():
    def gross_profit_margin(self, gross_profit, revenue):
        """[summary]

        Parameters
        ----------
        gross_profit : [type]
            [description]
        revenue : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        gross_profit_margin = gross_profit / revenue
        return gross_profit_margin

    def sga_expense_ratio(self, sga, revenue):
        """[summary]

        Parameters
        ----------
        sga : [type]
            [description]
        revenue : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        sga_expense_ratio = sga / revenue
        return sga_expense_ratio

    def rnd_expense_ratio(self, rnd, revenue):
        """[summary]

        Parameters
        ----------
        rnd : [type]
            [description]
        revenue : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        rnd_expense_ratio = rnd / revenue
        return rnd_expense_ratio

    def depreciation_expense_ratio(self, depreciation, revenue):
        """[summary]

        Parameters
        ----------
        depreciation : [type]
            [description]
        revenue : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        depreciation_expense_ratio = depreciation / revenue
        return depreciation_expense_ratio

    def interest_expense_ratio(self, interest, revenue):
        """[summary]

        Parameters
        ----------
        interest : [type]
            [description]
        revenue : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        interest_expense_ratio = interest / revenue
        return interest_expense_ratio

    def net_profit_margin(self, net_income, revenue):
        """[summary]

        Parameters
        ----------
        net_income : [type]
            [description]
        revenue : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        net_profit_margin = net_income / revenue
        return net_profit_margin

    def debt_to_eq_ratio(self, debt, equity):
        """[summary]

        Parameters
        ----------
        debt : [type]
            [description]
        equity : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        debt_to_eq_ratio = debt / equity
        return debt_to_eq_ratio

    def lt_debt_ratio(self, lt_debt, net_income):
        """[summary]

        Parameters
        ----------
        lt_debt : [type]
            [description]
        net_income : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        lt_debt_ratio = lt_debt / net_income
        return lt_debt_ratio

    def cf_coverage_ratio(self, op_cf, total_debt):
        """[summary]

        Parameters
        ----------
        op_cf : [type]
            [description]
        total_debt : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        cf_coverage_ratio = op_cf / total_debt
        return cf_coverage_ratio

    def return_on_equity(self, net_income, equity):
        """[summary]

        Parameters
        ----------
        net_income : [type]
            [description]
        equity : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        return_on_equity = net_income / equity
        return return_on_equity

    def return_capital_employed(self, ebit, total_assets, current_liabilities):
        """[summary]

        Parameters
        ----------
        ebit : [type]
            [description]
        total_assets : [type]
            [description]
        current_liabilities : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        return_capital_employed = ebit / (total_assets - current_liabilities)
        return return_capital_employed

    def return_net_assets(self, net_income, fixed_assets, net_working_capital):
        """[summary]

        Parameters
        ----------
        net_income : [type]
            [description]
        fixed_assets : [type]
            [description]
        net_working_capital : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        return_net_assets = net_income / (fixed_assets + net_working_capital)
        return return_net_assets

    def capital_expenditure_ratio(self, capital_expenditure, revenue):
        """[summary]

        Parameters
        ----------
        capital_expenditure : [type]
            [description]
        revenue : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        capital_expenditure = capital_expenditure / revenue
        return capital_expenditure

    def earnings_per_share(self):
        """[summary]

        Returns
        -------
        [type]
            [description]
        """

        return 0

    def company_repurchasing(self):
        """[summary]

        Returns
        -------
        [type]
            [description]
        """

        return 0

    def divident_netincome_ratio(self, divident_paid, net_income):
        """[summary]

        Parameters
        ----------
        divident_paid : [type]
            [description]
        net_income : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        divident_netincome_ratio = divident_paid / net_income
        return divident_netincome_ratio

    def fcfe(self, op_net_cash_flow, capital_expenditures):
        """[summary]

        Parameters
        ----------
        op_net_cash_flow : [type]
            [description]
        capital_expenditures : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        fcfe = 0
        return fcfe

    def market_timing(self, price, earnings_ratio):
        """[summary]

        Parameters
        ----------
        price : [type]
            [description]
        earnings_ratio : [type]
            [description]

        Returns
        -------
        [type]
            [description]
        """

        market_timing = 0
        return market_timing
