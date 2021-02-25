create_table_warren_investments = ''' 
        CREATE TABLE create_table_warren_investments( 
            year INTEGER, 
            shares INTEGER, 
            company STRING, 
            percentage_of_company_owned REAL, 
            cost_in_mio REAL,
            market_in_mio REAL,
            ticker STRING,
            net_change_shares INTEGER, 
            ) 
        '''


create_table_stocks = '''
            CREATE TABLE create_table_stocks(
                permo INTEGER,
                date INTEGER,
                ticker STRING,
                North_American_Industry_Class INTEGER,
                security_status STRING,
                header_sic_industry_group INTEGER,
                price DECIMAL(5, 4)
                volume INTEGER
                number_of_shares_outstanding INTEGER

            )
        '''
