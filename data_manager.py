import psycopg2
import os
import urllib
from connection_data import connection_data


def connect_heroku_pg():
    urllib.parse.uses_netloc.append('postgres')
    url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))
    connection = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return connection


def run_query(sql_query, variables=(), with_returnvalue=True):
    try:
        connect_str = "dbname='{}' user='{}' host='{}' password='{}'".format(*connection_data())
        connection = psycopg2.connect(connect_str)
        # connection = connect_heroku_pg()
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


def add_vote(user_id, planet_id, planet_name):
    sql_query = """
        INSERT INTO votes (user_id, planet_id, planet_name)
        VALUES (%s, %s, %s);
    """
    run_query(sql_query, (user_id, planet_id, planet_name), False)


def votable(planet_id, user_id):
    sql_query = """
        SELECT * FROM votes
        WHERE planet_id={} and user_id={};
    """.format(planet_id, user_id)
    votes = run_query(sql_query)
    result = False if votes else True
    return result


def get_statistics():
    sql_query = """
        SELECT planet_name, COUNT(*) as vote_count FROM votes
        GROUP BY planet_name
        ORDER BY vote_count desc;
    """
    result = run_query(sql_query)
    result = [{'name': planet[0], 'count': planet[1]}for planet in result]
    return result
