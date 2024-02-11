"""
12. Оцінки студентів у певній групі з певного предмета на останньому занятті.
"""

from connect import create_connection
import logging
from psycopg2 import DatabaseError

if __name__ == "__main__":
    sql_expression = """
    SELECT students.id, students.full_name AS student_name, groups.name AS group_name, subjects.name AS subject_name, grades.grade, grades.grade_date
    FROM students
    JOIN grades ON students.id = grades.student_id
    JOIN subjects ON grades.subject_id = subjects.id
    JOIN groups ON students.group_id = groups.id
    JOIN (
        SELECT student_id, subject_id, MAX(grade_date) AS last_lesson_date
        FROM grades
        GROUP BY student_id, subject_id
    ) AS last_lessons ON grades.student_id = last_lessons.student_id AND grades.subject_id = last_lessons.subject_id AND grades.grade_date = last_lessons.last_lesson_date
    WHERE groups.id = 1 AND subjects.id = 3;
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
