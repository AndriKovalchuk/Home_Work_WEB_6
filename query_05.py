"""
5. Знайти які курси читає певний викладач.
"""

from connect import create_connection
import logging
from psycopg2 import DatabaseError

if __name__ == '__main__':
    sql_expression = """
    SELECT subjects.name, teachers.full_name
    FROM subjects
    JOIN teachers ON subjects.teacher_id = teachers.id
    WHERE teachers.id = 1
    ORDER BY subjects.name;
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
