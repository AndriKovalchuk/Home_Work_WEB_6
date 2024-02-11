"""
1. Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
"""

from connect import create_connection
import logging
from psycopg2 import DatabaseError

if __name__ == "__main__":
    sql_expression = """
    SELECT students.id, students.full_name, ROUND(AVG(grades.grade), 2) AS average_grade
    FROM students
    JOIN grades ON students.id = grades.student_id
    GROUP BY students.id
    ORDER BY average_grade DESC
    LIMIT 5;
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
                logging.error("Could not connect to database")
    except RuntimeError as err:
        logging.error(err)
