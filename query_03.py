"""
3. Знайти середній бал у групах з певного предмета.
"""

from connect import create_connection
import logging
from psycopg2 import DatabaseError

if __name__ == '__main__':
    sql_expression = """
    SELECT ROUND(AVG(grades.grade), 2) AS average_grade, groups.name, subjects.name
    FROM grades
    JOIN students ON students.id = grades.student_id
    JOIN groups ON students.group_id = groups.id
    JOIN subjects ON grades.subject_id = subjects.id
    WHERE grades.subject_id = 3
    GROUP BY groups.id, groups.name, subjects.name
    ORDER BY average_grade DESC;
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
