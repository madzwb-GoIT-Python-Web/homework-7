import sqlalchemy as sa
import sqlalchemy.orm as orm
import sqlalchemy.ext.declarative as extension
from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, text, Identity

import registrator.registrator as registrator

Base    = extension.declarative_base()

class Group(Base):
    __tablename__ = "groups"
    id          = Column("id"         , Integer     , primary_key = True)#, autoincrement = True)
    name        = Column("name"       , String(128) , nullable=False    , unique=True)

    __table_args__ = (UniqueConstraint("name", name = "uc_groups")  ,)

    students    = orm.relationship("Student", back_populates="group")



class Student(Base):
    __tablename__ = "students"
    id          = Column("id"         , Integer     , primary_key = True)#, autoincrement = True)
    group_id    = Column("group_id"   , Integer     , ForeignKey('groups.id'    , onupdate="CASCADE"    , ondelete="CASCADE")   , nullable=False)
    first_name  = Column("first_name" , String(128) , nullable=False)
    last_name   = Column("last_name"  , String(128) , nullable=False)
    middle_name = Column("middle_name", String(128) , nullable=True)

    __table_args__ = (UniqueConstraint("first_name", "last_name", name = "uc_students") ,)

    group           = orm.relationship("Group"  , back_populates="students")
    student_scores  = orm.relationship("Score"  , back_populates="student")



class Teacher(Base):
    __tablename__ = "teachers"
    id          = Column("id"         , Integer     , primary_key = True, autoincrement = True)
    first_name  = Column("first_name" , String(128) , nullable=False)
    last_name   = Column("last_name"  , String(128) , nullable=False)
    middle_name = Column("middle_name", String(128) , nullable=True)

    __table_args__ = (UniqueConstraint("first_name", "last_name", name = "uc_teachers") ,)

    courses     = orm.relationship("Course", back_populates="teacher", uselist=False)



class Course(Base):
    __tablename__ = "courses"
    id          = Column("id"         , Integer     , primary_key = True, autoincrement = True)
    teacher_id  = Column("teacher_id" , Integer     , ForeignKey('teachers.id'  , onupdate="CASCADE"    , ondelete="CASCADE")   , nullable=False)
    name        = Column("name"       , String(128) , nullable=False    , unique=True)

    __table_args__ = (UniqueConstraint("name", name = "uc_courses") ,)  # Restrict to one-to-one
    # __table_args__ = UniqueConstraint("teacher_id", "name", name = "uc_courses")

    teacher         = orm.relationship("Teacher"    , back_populates="courses")
    course_scores   = orm.relationship("Score"      , back_populates="course")



class Score(Base):
    __tablename__ = "scores"
    id          = Column("id"         , Integer     , primary_key = True, autoincrement = True)
    course_id   = Column("course_id"  , Integer     , ForeignKey('courses.id'   , onupdate="CASCADE"    , ondelete="CASCADE")   , nullable=False)
    student_id  = Column("student_id" , Integer     , ForeignKey('students.id'  , onupdate="CASCADE"    , ondelete="CASCADE")   , nullable=False)
    datetime    = Column("datetime"   , DateTime    , nullable=False, server_default=text("CURRENT_TIMESTAMP"))
    score       = Column("score"      , Integer     , nullable=False)

    __table_args__ = (UniqueConstraint("course_id", "student_id", "datetime", name = "uc_scores")   ,)

    course      = orm.relationship("Course"    , back_populates="course_scores")
    student     = orm.relationship("Student"   , back_populates="student_scores")

metadata = MetaData()
# metadata = Base.metadata

class MODELS(registrator.REGISTRATOR):    ...
MODELS.register("", __name__, globals(), Base,["__builtins__", "Base"])
registry = MODELS()
