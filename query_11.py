"""
11. Середній бал, який певний викладач ставить певному студентові.
"""

from connect import create_connection
import logging
from psycopg2 import DatabaseError

if __name__ == "__main__":
    sql_expression = """
    SELECT ROUND(AVG(grades.grade), 2) AS average_grade, teachers.full_name AS teacher_name, students.full_name AS students_name
    FROM grades
    JOIN students ON grades.student_id = students.id
    JOIN subjects ON grades.subject_id = subjects.id
    JOIN teachers ON subjects.teacher_id = teachers.id
    WHERE teachers.id = 3 AND students.id = 3
    GROUP BY teacher_name, students_name
    ORDER BY average_grade;
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
