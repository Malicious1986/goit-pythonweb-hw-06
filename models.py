from __future__ import annotations

from datetime import datetime
from typing import List

from sqlalchemy import ForeignKey, Integer, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class Students(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    grades: Mapped[List["Grades"]] = relationship(back_populates="student")
    group_id: Mapped[int] = mapped_column(ForeignKey("groups.id"), nullable=False)
    group: Mapped["Groups"] = relationship(back_populates="students")


class Groups(Base):
    __tablename__ = "groups"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    students: Mapped[List["Students"]] = relationship(back_populates="group")


class Teachers(Base):
    __tablename__ = "teachers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    email: Mapped[str] = mapped_column(unique=True)
    subjects: Mapped[List["Subjects"]] = relationship(back_populates="teacher")


class Subjects(Base):
    __tablename__ = "subjects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True)
    teacher_id: Mapped[int] = mapped_column(ForeignKey("teachers.id"))
    teacher: Mapped["Teachers"] = relationship(back_populates="subjects")
    grades: Mapped[List["Grades"]] = relationship(back_populates="subject")


class Grades(Base):
    __tablename__ = "grades"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"))
    subject_id: Mapped[int] = mapped_column(ForeignKey("subjects.id"))
    value: Mapped[int] = mapped_column(Integer)
    received_at: Mapped[datetime] = mapped_column(default=datetime)

    student: Mapped["Students"] = relationship(back_populates="grades")
    subject: Mapped["Subjects"] = relationship(back_populates="grades")
