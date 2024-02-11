"""
7. Знайти оцінки студентів у окремій групі з певного предмета.
"""

from connect import create_connection
import logging
from psycopg2 import DatabaseError

if __name__ == '__main__':
    sql_expression = """
    SELECT students.id, students.full_name, grades.grade, groups.name, subjects.name
    FROM grades
    JOIN students ON grades.student_id = students.id
    JOIN groups ON students.group_id = groups.id
    JOIN subjects ON grades.subject_id = subjects.id
    WHERE groups.id = 1 AND subjects.id = 1
    ORDER BY students.id;
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
