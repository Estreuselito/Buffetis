import pandas as pd


class Cusips():
    """This class receives all ticker and cusips from Quarterly_investments
    """

    def __init__(self, connection):
        """Initializes the object with a database connection

        Parameters
        ----------
        connection : sqlite3.cursor
            This is the sqlite3.cursor for the database
        """
        self.connection = connection

    def get_all_cusips(self, string_number):
        """Receives all distinct CUSIPS from the Quarterly_investment table 

        Returns
        -------
        tuple
            A tuple with all distinct CUSIPS
        """
        # get cusips from Warren Buffets investment
        cusips_SEC_filings = pd.read_sql_query(
            f"SELECT DISTINCT SUBSTR(CUSIP_8Digits, 1, {string_number}) AS CUSIP FROM Quarterly_investments", self.connection)

        cusips_dict_SEC_filings = cusips_SEC_filings.to_dict(orient='list')

        cusips_SEC_filings = cusips_dict_SEC_filings['CUSIP']

        # merge both cusip sources and filter the duplicates
        total_cusips = [x for x in cusips_SEC_filings if x is not None]

        return tuple(total_cusips)

    def get_all_ticker(self):
        """Receives all the distinct tickers from the fundamentals_a table

        Returns
        -------
        tuple
            Returns a tuple with all the distinct tickers from the fundamentals_a table 
        """

        ticker_fundamentals = pd.read_sql_query(
            "SELECT DISTINCT ticker FROM fundamentals_a", self.connection)

        ticker_dict_fundamentals = ticker_fundamentals.to_dict(orient='list')

        ticker_fundamentals = ticker_dict_fundamentals['ticker']

        return tuple(ticker_fundamentals)
