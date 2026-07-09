import mysql.connector


def get_connection():

    connection = mysql.connector.connect(
        host="localhost",
        user="supermarket_user",
        password="supermarket123",
        database="DATA_ENG_PROJ"
    )

    return connection
