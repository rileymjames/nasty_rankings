import psycopg2
import pandas as pd
from sqlalchemy import create_engine


def deploy_sql_table(hostname, database, user, password, portno, sql):
    '''
    Deploys a SQL table to a PostgreSQL Server.

    Parameters
    ----------
    hostname : str
        Hostname to connect to.
    database : str
        Name of database to connect to.
    user : str
        Username to apply to make connection.
    password : str
        Password to apply to make connection.
    portno : int
        Port number of the server.
    sql : str
        SQL to deploy.

    Returns
    -------
    None
    '''

    conn = psycopg2.connect(database=database, user=user, password=password,
                            host=hostname, port=portno)

    cursor = conn.cursor()

    cursor.execute(sql)
    conn.commit()

    conn.close()

    return
