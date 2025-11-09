import sys

from models import Students, Grades, Subjects, Groups, Teachers
from connect import session
from sqlalchemy import select, func, desc


def select_1():
    stmt = (
        select(
            Students.id,
            Students.name,
            Students.email,
            func.avg(Grades.value).label("avg_grade"),
        )
        .join(Grades, Grades.student_id == Students.id)
        .group_by(Students.id)
        .order_by(desc(func.avg(Grades.value)))
        .limit(5)
    )

    results = session.execute(stmt).all()
    return results


def select_2(subject_name: str):
    stmt = (
        select(
            Students.id,
            Students.name,
            Students.email,
            func.avg(Grades.value).label("avg_grade"),
        )
        .join(Grades, Grades.student_id == Students.id)
        .join(Subjects, Subjects.id == Grades.subject_id)
        .where(Subjects.name == subject_name)
        .group_by(Students.id)
        .order_by(desc(func.avg(Grades.value)))
        .limit(1)
    )

    result = session.execute(stmt).first()
    return result


def select_3(subject_name: str):
    stmt = (
        select(
            Groups.id,
            Groups.name,
            func.avg(Grades.value).label("avg_grade"),
        )
        .join(Students, Students.group_id == Groups.id)
        .join(Grades, Grades.student_id == Students.id)
        .join(Subjects, Subjects.id == Grades.subject_id)
        .where(Subjects.name == subject_name)
        .group_by(Groups.id)
        .order_by(desc(func.avg(Grades.value)))
    )

    results = session.execute(stmt).all()
    return results


def select_4():
    stmt = select(func.avg(Grades.value).label("avg"))
    avg = session.execute(stmt).scalar()
    return avg


def select_5(teacher_name: str):
    stmt = (
        select(Subjects.id, Subjects.name)
        .join(Teachers, Subjects.teacher_id == Teachers.id)
        .where(Teachers.name == teacher_name)
    )
    return session.execute(stmt).all()


def select_6(group_name: str):
    stmt = (
        select(Students.id, Students.name, Students.email)
        .join(Groups, Students.group_id == Groups.id)
        .where(Groups.name == group_name)
    )
    return session.execute(stmt).all()


def select_7(group_name: str, subject_name: str):
    stmt = (
        select(
            Students.id,
            Students.name,
            Grades.value,
            Grades.received_at,
        )
        .join(Groups, Students.group_id == Groups.id)
        .join(Grades, Grades.student_id == Students.id)
        .join(Subjects, Subjects.id == Grades.subject_id)
        .where(Groups.name == group_name, Subjects.name == subject_name)
        .order_by(Students.id)
    )
    return session.execute(stmt).all()


def select_8(teacher_name: str):
    stmt = (
        select(func.avg(Grades.value).label("avg"))
        .join(Subjects, Subjects.id == Grades.subject_id)
        .join(Teachers, Subjects.teacher_id == Teachers.id)
        .where(Teachers.name == teacher_name)
    )
    return session.execute(stmt).scalar()


def select_9(student_name: str):
    stmt = (
        select(Subjects.id, Subjects.name)
        .join(Grades, Grades.subject_id == Subjects.id)
        .join(Students, Grades.student_id == Students.id)
        .where(Students.name == student_name)
        .group_by(Subjects.id)
    )
    return session.execute(stmt).all()


def select_10(student_name: str, teacher_name: str):
    stmt = (
        select(Subjects.id, Subjects.name)
        .join(Grades, Grades.subject_id == Subjects.id)
        .join(Students, Grades.student_id == Students.id)
        .join(Teachers, Subjects.teacher_id == Teachers.id)
        .where(Students.name == student_name, Teachers.name == teacher_name)
        .group_by(Subjects.id)
    )
    return session.execute(stmt).all()
