import pandas as pd
from sqlalchemy import create_engine
from config import db_host, db_name, db_password, db_port, db_user


import psycopg2


from functools import wraps


def db_connect(func):
    @wraps(func)
    def with_connection(*args, **kwargs):
        conn = None
        try:
            conn = psycopg2.connect(
                dbname=db_name,
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port
            )
            result = func(conn, *args, **kwargs)
            return result
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            if conn:
                conn.close()
    return with_connection


@db_connect
def execute_query(conn, query):
    with conn.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
        result = [row[0] for row in result]
        return result


def get_df_from_db(query):
    db_connection_string= f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    engine = create_engine(db_connection_string)
    df = pd.read_sql(query, engine)
    return df