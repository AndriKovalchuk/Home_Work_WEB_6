from contextlib import contextmanager
import psycopg2


@contextmanager
def create_connection():
    try:
        """ create a connection to database"""
        connection = psycopg2.connect(host='localhost', database='faculty', user='postgres', password='1234')
        yield connection
        connection.close()
    except psycopg2.OperationalError as err:
        raise RuntimeError(f'Failed to create a connection with database: {err}')
