from connect import create_connection
from faker import Faker
import logging
from psycopg2 import DatabaseError
from random import randint

STUDENTS = 45
GROUPS = 3
SUBJECTS = 6
TEACHERS = 3
GRADES = 8_000

fake = Faker('uk-Ua')


def insert_data(connection, sql_expression):
    c = connection.cursor()
    try:
        if sql_expression == sql_insert_groups_data:
            for _ in range(GROUPS):
                c.execute(sql_expression, (fake.word(),))

        elif sql_expression == sql_insert_teachers_data:
            for _ in range(TEACHERS):
                c.execute(sql_insert_teachers_data, (fake.name(),))

        elif sql_expression == sql_insert_subjects_data:
            for teacher_id in range(1, TEACHERS + 1):
                for _ in range(2):
                    c.execute(sql_insert_subjects_data, (fake.job(), teacher_id))

        elif sql_expression == sql_insert_students_data:
            for group_id in range(1, GROUPS + 1):
                for _ in range(15):
                    c.execute(sql_insert_students_data, (fake.name(), group_id))
                    id = c.fetchone()[0]

        elif sql_expression == sql_insert_grades_data:
            for _ in range(3):
                for student_id in range(1, STUDENTS + 1):
                    for subject_id in range(1, SUBJECTS + 1):
                        c.execute(sql_insert_grades_data,
                                  (student_id, subject_id, randint(0, 100), fake.date_this_year()))

        connection.commit()
    except DatabaseError as e:
        logging.error(e)
        connection.rollback()
    finally:
        c.close()


if __name__ == '__main__':
    sql_insert_groups_data = """
    INSERT INTO groups (name) VALUES (%s);
    """

    sql_insert_teachers_data = """
        INSERT INTO teachers (full_name) VALUES (%s);
        """

    sql_insert_subjects_data = """
        INSERT INTO subjects (name, teacher_id) VALUES (%s, %s);
        """

    sql_insert_students_data = """
    INSERT INTO students (full_name, group_id) VALUES (%s, %s) RETURNING id;
    """

    sql_insert_grades_data = """
            INSERT INTO grades (student_id, subject_id, grade, grade_date) VALUES (%s, %s, %s, %s);
            """

    try:
        with create_connection() as connection:
            if connection is not None:
                insert_data(connection, sql_insert_groups_data)
                insert_data(connection, sql_insert_teachers_data)
                insert_data(connection, sql_insert_subjects_data)
                insert_data(connection, sql_insert_students_data)
                insert_data(connection, sql_insert_grades_data)
            else:
                logging.error('Could not connect to database')
    except RuntimeError as err:
        logging.error(err)
