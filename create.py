from connect import create_connection
import logging
from psycopg2 import DatabaseError


def create_table(connection, sql_expression: str):
    c = connection.cursor()
    try:
        c.execute(sql_expression)
        connection.commit()
    except DatabaseError as e:
        logging.error(e)
        connection.rollback()
    finally:
        c.close()


if __name__ == "__main__":
    # GROUPS
    sql_create_groups_table = """
    DROP TABLE IF EXISTS groups;
    CREATE TABLE IF NOT EXISTS groups (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) NOT NULL
    );
    """

    # STUDENTS
    sql_create_students_table = """
        DROP TABLE IF EXISTS students;
        CREATE TABLE IF NOT EXISTS students (
        id SERIAL PRIMARY KEY,
        full_name VARCHAR(150) NOT NULL,
        group_id INTEGER REFERENCES groups(id)
        );
        """

    # TEACHERS
    sql_create_teachers_table = """
            DROP TABLE IF EXISTS teachers;
            CREATE TABLE IF NOT EXISTS teachers (
            id SERIAL PRIMARY KEY,
            full_name VARCHAR(150) NOT NULL
            );
            """

    # SUBJECTS
    sql_create_subjects_table = """
                DROP TABLE IF EXISTS subjects;
                CREATE TABLE IF NOT EXISTS subjects (
                id SERIAL PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                teacher_id INTEGER REFERENCES teachers(id)
                );
                """

    # GRADES
    sql_create_grades_table = """
                    DROP TABLE IF EXISTS grades;
                    CREATE TABLE IF NOT EXISTS grades (
                    id SERIAL PRIMARY KEY,
                    student_id INTEGER REFERENCES students(id),
                    subject_id INTEGER REFERENCES subjects(id),
                    grade NUMERIC CHECK(grade >=0 AND grade <= 100),
                    grade_date DATE NOT NULL
                    );
                    """

    try:
        with create_connection() as connection:
            if connection is not None:
                create_table(connection, sql_create_groups_table)
                create_table(connection, sql_create_students_table)
                create_table(connection, sql_create_teachers_table)
                create_table(connection, sql_create_subjects_table)
                create_table(connection, sql_create_grades_table)
            else:
                logging.error("Could not connect to database")
    except RuntimeError as err:
        logging.error(err)
