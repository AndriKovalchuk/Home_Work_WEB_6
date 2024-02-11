"""
9. Знайти список курсів, які відвідує студент.
"""

from connect import create_connection
import logging
from psycopg2 import DatabaseError

if __name__ == '__main__':
    sql_expression = """
    SELECT students.id, students.full_name, subjects.name as course_name
    FROM students
    JOIN grades ON students.id = grades.student_id
    JOIN subjects ON grades.subject_id = students.id
    WHERE students.id = 1
    GROUP BY students.id, students.full_name, subjects.name
    ORDER BY students.full_name;
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
