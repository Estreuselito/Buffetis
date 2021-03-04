class Financial_ratios():
    def gross_profit_margin(self, gross_profit, revenue):
        """Gross profit is the profit a company makes after \
            deducting the costs associated with making and \
            selling its products, or the costs associated \
            with providing its services. Gross profit will \
            appear on a company's income statement and can \
            be calculated by subtracting the cost of goods \
            sold (COGS) from revenue (sales). These figures \
            can be found on a company's income statement. \
            (https://www.investopedia.com/terms/g/grossprofit.asp)

        Parameters
        ----------
        gross_profit : pd.Series of ints
            This is the gross profit of the companies
        revenue : pd.Series of ints
            This is the revenue for the companies

        Returns
        -------
        pd.Series of ints
            The gross profit margin for each company
        """

        gross_profit_margin = gross_profit / revenue
        return gross_profit_margin

    def sga_expense_ratio(self, sga, revenue):
        """Selling, general and administrative expense (SG&A) \
           is reported on the income statement as the sum of \
           all direct and indirect selling expenses and all \
           general and administrative expenses (G&A) of a \
           company. SG&A, also known as SGA, includes all \
           the costs not directly tied to making a product \
           or performing a service. That is, SG&A includes \
           the costs to sell and deliver products and services \
           and the costs to manage the company.  \
           (https://www.investopedia.com/terms/s/sga.asp)

        Parameters
        ----------
        sga : pd.Series of ints
            These are the accumalted SG&A costs for the different \
            companies
        revenue : pd.Series of ints
            This the revenue of those companies

        Returns
        -------
        pd.Series of ints
            The SG&A expense ratio
        """

        sga_expense_ratio = sga / revenue
        return sga_expense_ratio

    def rnd_expense_ratio(self, rnd, revenue):
        """This metric is useful in comparing the effectiveness \
           of R&D expenditures between companies in the same \
           industry. It is less obvious across industries - for \
           example, pharmaceuticals and software companies tend \
           to spend a lot on R&D while consumer product companies \
           spent less. \
           (https://www.stockopedia.com/ratios/research-development-to-sales-5090/)

        Parameters
        ----------
        rnd : pd.Series of ints
            The money which were invested into Research & Development
        revenue : pd.Series of ints
            The revenue a company made

        Returns
        -------
        pd.Series of ints
            How much money were returned by investing into R&D
        """

        rnd_expense_ratio = rnd / revenue
        return rnd_expense_ratio

    def depreciation_expense_ratio(self, depreciation, revenue):
        """Depreciation-Expense Ratio is measured as a percentage, \
           the lower the percentage the stronger the ratio. The \
           Depreciation-Expense Ratio intimates the amount of income \
           that is required to maintain the capital being used by the \
           business or farm. The lower the percentages the better, a \
           business or farm should be no higher than 5% to be considered \
           strong. Any percentage higher than 15% means that the business \
           or farm may be wearing out its capital to quickly. \
           (https://www.canr.msu.edu/news/financial_ratios_part_19_of_21_depreciation_expense_ratio)

        Parameters
        ----------
        depreciation : pd.Series of ints
            The amount which will be depreciated
        revenue : pd.Series of ints
            The revenue a company made

        Returns
        -------
        pd.Series of ints
            The depreciation expense ratio
        """

        depreciation_expense_ratio = depreciation / revenue
        return depreciation_expense_ratio

    def interest_expense_ratio(self, interest, revenue):
        """[summary]

        Parameters
        ----------
        interest : pd.Series of ints
            The interest a company has to pay
        revenue : pd.Series of ints
            The revenue a company made

        Returns
        -------
        pd.Series of ints
            The interest expense ratio
        """

        interest_expense_ratio = interest / revenue
        return interest_expense_ratio

    def net_profit_margin(self, net_income, revenue):
        """The net profit margin, or simply net margin, \
           is equal to how much net income or profit is \
           generated as a percentage of revenue. Net \
           profit margin is the ratio of net profits \
           to revenues for a company or business segment. \
           Net profit margin is typically expressed as a \
           percentage but can also be represented in decimal \
           form. The net profit margin illustrates how \
           much of each dollar in revenue collected by \
           a company translates into profit.\
           (https://www.investopedia.com/terms/n/net_margin.asp)

        Parameters
        ----------
        net_income : pd.Series of ints
            The overall net income by a company
        revenue : pd.Series of ints
            The revenue a company made

        Returns
        -------
        pd.Series of ints
            The percentage of net income on revenue
        """

        net_profit_margin = net_income / revenue
        return net_profit_margin

    def debt_to_eq_ratio(self, debt, equity):
        """The ratio is used to evaluate a company's \
           financial leverage. The D/E ratio is an \
           important metric used in corporate finance. \
           It is a measure of the degree to which a \
           company is financing its operations through \
           debt versus wholly-owned funds. More specifically, \
           it reflects the ability of shareholder equity to \
           cover all outstanding debts in the event of \
           a business downturn.\
           (https://www.investopedia.com/terms/d/debtequityratio.asp)

        Parameters
        ----------
        debt : pd.Series of ints
            The overall debt a company has
        equity : pd.Series of ints
            The equity a company owns

        Returns
        -------
        pd.Series of ints
            The ratio on whether or not a company is
            able to finance its own operations
        """

        debt_to_eq_ratio = debt / equity
        return debt_to_eq_ratio

    def lt_debt_ratio(self, lt_debt, net_income):
        """The long-term debt-to-total-assets ratio \
           is a measurement representing the percentage \
           of a corporation's assets financed with \
           long-term debt, which encompasses loans \
           or other debt obligations lasting more than \
           one year. This ratio provides a general \
           measure of the long-term financial position \
           of a company, including its ability to meet \
           its financial obligations for outstanding \
           loans.\
           (https://www.investopedia.com/terms/l/long-term-debt-to-total-assets-ratio.asp)

        Parameters
        ----------
        lt_debt : pd.Series of ints
            The long term debts
        net_income : pd.Series of ints
            The total net income from a company

        Returns
        -------
        pd.Series of ints
            Returns the ratio between the own owned
            assets to the ones' owned from a debt
        """

        lt_debt_ratio = lt_debt / net_income
        return lt_debt_ratio

    def cf_coverage_ratio(self, op_cf, total_debt):
        """The cash flow-to-debt ratio is the ratio of \
           a company’s cash flow from operations to its \
           total debt. This ratio is a type of coverage \
           ratio and can be used to determine how long \
           it would take a company to repay its debt if \
           it devoted all of its cash flow to debt repayment. \
           Cash flow is used rather than earnings because \
           cash flow provides a better estimate of a company’s \
           ability to pay its obligations.\
           (https://www.investopedia.com/terms/c/cash-flowtodebt-ratio.asp)


        Parameters
        ----------
        op_cf : pd.Series of ints
            The total cash flow from the operating business
        total_debt : pd.Series of ints
            The total debt a company has

        Returns
        -------
        pd.Series of ints
            How long would a company need to repay all \
            its debt, if it would devote all his operating \
            cash flows towards repaying those
        """

        cf_coverage_ratio = op_cf / total_debt
        return cf_coverage_ratio

    def return_on_equity(self, net_income, equity):
        """Return on equity (ROE) is a measure of financial performance \
           calculated by dividing net income by shareholders' equity. \
           Because shareholders' equity is equal to a company’s assets \
           minus its debt, ROE is considered the return on net assets. \
           ROE is considered a measure of the profitability of a corporation \
           in relation to stockholders’ equity.\
           (https://www.investopedia.com/terms/r/returnonequity.asp)

        Parameters
        ----------
        net_income : pd.Series of ints
            The total net income from a company
        equity : pd.Series of ints
            The equity a company owns

        Returns
        -------
        pd.Series of ints
            The return on equity
        """

        return_on_equity = net_income / equity
        return return_on_equity

    def return_capital_employed(self, ebit, total_assets, current_liabilities):
        """Return on capital employed (ROCE) is a financial ratio that can be \
           used in assessing a company's profitability and capital efficiency. \
           In other words, this ratio can help to understand how well a \
           company is generating profits from its capital as it is put to use.\
           (https://www.investopedia.com/terms/r/roce.asp)

        Parameters
        ----------
        ebit : pd.Series of ints
            [description]
        total_assets : pd.Series of ints
            [description]
        current_liabilities : pd.Series of ints
            [description]

        Returns
        -------
        pd.Series of ints
            [description]
        """

        return_capital_employed = ebit / (total_assets - current_liabilities)
        return return_capital_employed

    def return_net_assets(self, net_income, fixed_assets, net_working_capital):
        """Return on net assets (RONA) is a measure of financial performance \
           calculated as net profit divided by the sum of fixed assets and \
           net working capital. Net profit is also called net income.\
           The RONA ratio shows how well a company and its management \
           are deploying assets in economically valuable ways; a \
           high ratio result indicates that management is \
           squeezing more earnings out of each dollar invested \
           in assets. RONA is also used to assess how well a company \
           is performing compared to others in its industry.\
           (https://www.investopedia.com/terms/r/rona.asp)

        Parameters
        ----------
        net_income : pd.Series of ints
            The total net income from a company
        fixed_assets : pd.Series of ints
            The amount of fixed assests of a company
        net_working_capital : pd.Series of ints
            The net working capital of a company

        Returns
        -------
        pd.Series of ints
            Measure which can be compared to other firms in \
            that same industry.
        """

        return_net_assets = net_income / (fixed_assets + net_working_capital)
        return return_net_assets

    def capital_expenditure_ratio(self, capital_expenditure, revenue):
        """Cash flow to capital expenditures—CF/CapEX—is a ratio that \
           measures a company's ability to acquire long-term assets \
           using free cash flow. The CF/CapEX ratio will often fluctuate \
           as businesses go through cycles of large and small capital \
           expenditures. A higher CF/CapEX ratio is indicative of a \
           company with sufficient capital to fund operations.\
           (https://www.investopedia.com/terms/c/cashflow_capex.asp)

        Parameters
        ----------
        capital_expenditure : pd.Series of ints
            [description]
        revenue : pd.Series of ints
            The revenue a company made

        Returns
        -------
        pd.Series of ints
            [description]
        """

        capital_expenditure = capital_expenditure / revenue
        return capital_expenditure

    def earnings_per_share(self):
        """Earnings per share (EPS) is calculated as a company's \
           profit divided by the outstanding shares of its common \
           stock. The resulting number serves as an indicator of \
           a company's profitability. It is common for a company \
           to report EPS that is adjusted for extraordinary \
           items and potential share dilution. The higher a \
           company's EPS, the more profitable it is considered \
           to be.\
           (https://www.investopedia.com/terms/e/eps.asp)

        Returns
        -------
        pd.Series of ints
            [description]
        """

        return 0

    def company_repurchasing(self):
        """A share repurchase is a transaction whereby a \
           company buys back its own shares from the \
           marketplace. A company might buy back its \
           shares because management considers them \
           undervalued. The company buys shares directly \
           from the market or offers its shareholders the \
           option of tendering their shares directly to \
           the company at a fixed price.\
           Also known as a share buyback, this action \
           reduces the number of outstanding shares, which \
           increases both the demand for the shares and \
           the price.\
           (https://www.investopedia.com/terms/s/sharerepurchase.asp)

        Returns
        -------
        pd.Series of ints
            [description]
        """

        return 0

    def divident_netincome_ratio(self, divident_paid, net_income):
        """The dividend payout ratio is the ratio of the total \
           amount of dividends paid out to shareholders relative \
           to the net income of the company. It is the percentage \
           of earnings paid to shareholders in dividends. The \
           amount that is not paid to shareholders is retained \
           by the company to pay off debt or to reinvest in \
           core operations. It is sometimes simply referred \
           to as the 'payout ratio.'\
           The dividend payout ratio provides an indication \
           of how much money a company is returning to \
           shareholders versus how much it is keeping on \
           hand to reinvest in growth, pay off debt, or \
           add to cash reserves (retained earnings). \
           (https://www.investopedia.com/terms/d/dividendpayoutratio.asp)

        Parameters
        ----------
        divident_paid : pd.Series of ints
            [description]
        net_income : pd.Series of ints
            [description]

        Returns
        -------
        pd.Series of ints
            [description]
        """

        divident_netincome_ratio = divident_paid / net_income
        return divident_netincome_ratio

    def fcfe(self, op_net_cash_flow, capital_expenditures):
        """Free cash flow to equity is a measure of how much \
           cash is available to the equity shareholders of a \
           company after all expenses, reinvestment, and debt \
           are paid. FCFE is a measure of equity capital usage.\
\
           Free cash flow to equity is composed of net income, \
           capital expenditures, working capital, and debt. \
           Net income is located on the company income statement. \
           Capital expenditures can be found within the cash \
           flows from the investing section on the cash flow \
           statement.\
\
           Working capital is also found on the cash flow statement; \
           however, it is in the cash flows from the operations \
           section. In general, working capital represents the \
           difference between the company’s most current assets \
           and liabilities.\
           (https://www.investopedia.com/terms/f/freecashflowtoequity.asp)

        Parameters
        ----------
        op_net_cash_flow : pd.Series of ints
            [description]
        capital_expenditures : pd.Series of ints
            [description]

        Returns
        -------
        pd.Series of ints
            [description]
        """

        fcfe = 0
        return fcfe

    def market_timing(self, price, earnings_ratio):
        """Market timing is a type of investment or \
           trading strategy. It is the act of moving \
           in and out of a financial market or \
           switching between asset classes based on \
           predictive methods. These predictive tools \ 
           include following technical indicators or \
           economic data, to gauge how the market is \
           going to move.\
\
           Many investors, academics, and financial \
           professionals believe it is impossible to \
           time the market. Other investors, notably \
           active traders, believe strongly in it. \
           Thus, whether market timing is possible \
           is a matter of opinion. What can be said \
           with certainty is it is very difficult to \
           time the market consistently over the \
           long run successfully. \
\
           Market timing is the opposite of a \
           buy-and-hold investment strategy.\
           (https://www.investopedia.com/terms/m/markettiming.asp)

        Parameters
        ----------
        price : pd.Series of ints
            [description]
        earnings_ratio : pd.Series of ints
            [description]

        Returns
        -------
        pd.Series of ints
            [description]
        """

        market_timing = 0
        return market_timing
