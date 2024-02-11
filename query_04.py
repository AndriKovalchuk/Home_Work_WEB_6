"""
4. Знайти середній бал на потоці (по всій таблиці оцінок).
"""

from connect import create_connection
import logging
from psycopg2 import DatabaseError

if __name__ == '__main__':
    sql_expression = """
    SELECT ROUND(AVG(grades.grade), 2) AS average_grade
    FROM grades
    """

    try:
        with create_connection() as connection:
            if connection is not None:
                c = connection.cursor()
                try:
                    c.execute(sql_expression)
                    result = c.fetchall()
                    print(result)
                except DatabaseError as err:
                    logging.error(err)
                finally:
                    c.close()
            else:
                logging.error('Could not connect to database')
    except RuntimeError as err:
        logging.error(err)
