"""
2. Знайти студента із найвищим середнім балом з певного предмета.
"""

from connect import create_connection
import logging
from psycopg2 import DatabaseError

if __name__ == '__main__':
    sql_expression = """
    SELECT students.id, students.full_name, ROUND(AVG(grades.grade), 2) AS average_grade, subjects.name
    FROM grades
    JOIN students ON students.id = grades.student_id
    JOIN subjects ON grades.subject_id = subjects.id
    WHERE grades.subject_id = 6
    GROUP BY students.id, subjects.name
    ORDER BY average_grade DESC
    LIMIT 1;
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
