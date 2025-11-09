import random

from faker import Faker
from sqlalchemy import delete
from sqlalchemy.orm import Session
from connect import session

from models import Students, Groups, Teachers, Subjects, Grades

faker = Faker()

NUM_GROUPS = 3
NUM_TEACHERS_MIN = 3
NUM_TEACHERS_MAX = 5
NUM_SUBJECTS_MIN = 5
NUM_SUBJECTS_MAX = 8
NUM_STUDENTS_MIN = 30
NUM_STUDENTS_MAX = 50
MIN_GRADES_PER_STUDENT = 5
MAX_GRADES_PER_STUDENT = 20


def clear_existing(session: Session):
    session.execute(delete(Grades))
    session.execute(delete(Students))
    session.execute(delete(Subjects))
    session.execute(delete(Teachers))
    session.execute(delete(Groups))
    session.commit()


def seed():
    clear_existing(session)
    groups = [Groups(name=f"Group {i+1}") for i in range(NUM_GROUPS)]
    session.add_all(groups)

    # teachers
    num_teachers = random.randint(NUM_TEACHERS_MIN, NUM_TEACHERS_MAX)
    teachers = []
    for _ in range(num_teachers):
        t = Teachers(name=faker.name(), email=faker.unique.email())
        teachers.append(t)
    session.add_all(teachers)

    # subjects
    num_subjects = random.randint(NUM_SUBJECTS_MIN, NUM_SUBJECTS_MAX)
    subjects = []
    for _ in range(num_subjects):
        subj = Subjects(
            name=faker.unique.word().capitalize(), teacher=random.choice(teachers)
        )
        subjects.append(subj)
    session.add_all(subjects)

    # students
    num_students = random.randint(NUM_STUDENTS_MIN, NUM_STUDENTS_MAX)
    students = []
    for _ in range(num_students):
        s = Students(
            name=faker.name(),
            email=faker.unique.email(),
            group=random.choice(groups),
        )
        students.append(s)
    session.add_all(students)

    # grades:
    grades = []
    for s in students:
        n_grades = random.randint(MIN_GRADES_PER_STUDENT, MAX_GRADES_PER_STUDENT)
        for _ in range(n_grades):
            subject = random.choice(subjects)
            value = random.randint(1, 100)
            received_at = faker.date_time_between(start_date="-1y", end_date="now")
            g = Grades(student=s, subject=subject, value=value, received_at=received_at)
            grades.append(g)
    session.add_all(grades)
    session.commit()

    print(
        f"Seeded DB: {len(groups)} groups, {len(teachers)} teachers, {len(subjects)} subjects, {len(students)} students, {len(grades)} grades"
    )


if __name__ == "__main__":
    seed()
