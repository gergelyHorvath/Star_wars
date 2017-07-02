import psycopg2
from connection_data import connection_data


def run_query(sql_query, variables=(), with_returnvalue=True):
    try:
        connect_str = "dbname='{}' user='{}' host='{}' password='{}'".format(*connection_data())
        connection = psycopg2.connect(connect_str)
        connection.autocommit = True
        cursor = connection.cursor()
        cursor.execute(sql_query, variables)
        if with_returnvalue:
            data_table = cursor.fetchall()
        cursor.close()
    except psycopg2.DatabaseError as exception:
        print(exception)
    finally:
        if connection:
            connection.close()
    if with_returnvalue:
        return data_table


def get_users():
    sql_query = "SELECT * FROM users;"
    result = run_query(sql_query)
    return result


def add_user(username, password):
    sql_query = """
        INSERT INTO users (username, password)
        VALUES (%s, %s);
    """
    run_query(sql_query, (username, password), False)
