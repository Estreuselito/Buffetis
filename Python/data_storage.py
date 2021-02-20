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
