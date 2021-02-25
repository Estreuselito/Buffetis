# This script contains a function and a function statement
# which automatically creates the connection to the database
# Buffet or creates it, if it is not existant in the folder
# database.

import sqlite3
import os


def create_connection(db_name):
    """create a database connection to the SQLite database specified by db_name

    Parameters
    ----------
    db_name: str
        database name

    Returns
    -------
    c: connection object
        conn.cursor

    conn: connection
        direct connect to database
    """
    conn = sqlite3.connect(db_name, check_same_thread=False)

    return conn


if not os.path.exists("./database"):
    os.makedirs("./database")

connection = create_connection("./database/Buffet.db")


def check_and_create_and_insert(conn, table_name, df, sql_table_creating_string):
    """Check if table already exists, and when not create it
    Parameters
    ---------
    conn: connection
        Connection to database
    table_name: str
        the name of the table which shall be checked and/or created
    df: dataframe
        the dataframe, which should be saved into the database
    sql_table_createing_string: str
        a string literal of SQL command, in order to create a table    
    Returns
    -------
    None 
    """
    if table_exists(table_name, conn):
        print("Table already exists!")
        return None
    else:
        conn.execute(sql_table_creating_string)
        df.to_sql(name=table_name, con=conn, if_exists='append', index=False)
        print("Table is created!")
        return None
