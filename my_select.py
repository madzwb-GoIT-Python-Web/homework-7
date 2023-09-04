# import functools
import sqlalchemy.sql.functions as func

from sqlalchemy import select, func, desc, DATE, and_, true
# from sqlalchemy.orm import aliased

# import model
from connection import session
from models import Group, Student, Teacher, Course, Score

def select_01(criterion = None):
    """Returns first five studens with highest average score."""
    results = session().query(
        Student.first_name,
        Student.last_name,
        func.round(func.avg(Score.score), 2).label('average_score'),
        func.count('*')
    ).select_from(Score).join(Student)\
        .filter(criterion if criterion is not None else true())\
        .group_by(Student.id)\
        .order_by(desc('average_score')).limit(5)
    return results

def select_02(criterion = None):
    """Returns first student with highest average score by course."""
    # filters = [getattr(Score, name) == value for (name, value) in kwargs.items()]
    results = session().query(
        Course.id,
        Course.name,
        Student.first_name,
        Student.last_name,
        func.round(func.avg(Score.score), 2).label('average_score'),
        func.count('*'),
    ).select_from(Score).join(Student).join(Course)\
        .filter(criterion if criterion is not None else true())\
        .group_by(Course.name, Student.id)\
        .order_by(desc('average_score')).limit(1)
    return results

def select_03(criterion = None):#**kwargs):
    """Returns average score in groups by courses."""
    # filters = [getattr(Score, name) == value for (name, value) in kwargs.items()]
    results = session().query(
        Group.name,
        Course.id,
        Course.name,
        func.round(func.avg(Score.score), 2).label('average_score'),
        func.count('*')
    ).select_from(Score).join(Student).join(Group).join(Course)\
        .filter(criterion if criterion is not None else true())\
        .group_by(Group.id, Group.name, Course.id, Course.name)\
        .order_by(Group.id, Course.id)
    return results

def select_04(criterion = None):#**kwargs):
    """Returns average score."""
    results = session().query(
        func.round(func.avg(Score.score), 2).label('average_score')
    ).select_from(Score)
    return results

def select_05(criterion = None):#**kwargs):
    """Returns courses taught by the teacher."""
    # filters = [getattr(Teacher, name) == value for (name, value) in kwargs.items()]
    results = session().query(
        Teacher.first_name,
        Teacher.last_name,
        Course.name
    ).select_from(Teacher).join(Course)\
        .filter(criterion if criterion is not None else true())
    return results

def select_06(criterion = None):#**kwargs):
    """Returns students in the group."""
    # filters = [getattr(Group, name) == value for (name, value) in kwargs.items()]
    results = session().query(
        Group.name,
        Student.first_name,
        Student.last_name
    ).select_from(Group).join(Student)\
        .filter(criterion if criterion is not None else true())
    return results

def select_07(criterion = None):
    """Returns scores of group by course."""
    # filters = [getattr(Course, name) == value for (name, value) in kwargs.items()]
    results = session().query(
        Group.name,
        Course.name,
        Student.first_name,
        Student.last_name,
        Score.score,
        Score.datetime
    ).select_from(Score).join(Course).join(Student).join(Group)\
        .filter(criterion if criterion is not None else true())
    return results

def select_08(criterion = None):
    """Returns average score given by teacher for his courses."""
    results = session().query(
        Course.name,
        Teacher.first_name,
        Teacher.last_name,
        func.round(func.avg(Score.score), 2).label('average_score'),
        func.count('*')
    ).select_from(Score).join(Course).join(Teacher)\
        .group_by(Teacher.id, Course.id)\
        .filter(criterion if criterion is not None else true())
    return results

def select_09(criterion = None):
    """Returns courses attended by the student."""
    results = session().query(
        Student.first_name,
        Student.last_name,
        Course.name,
    ).select_from(Score).join(Course).join(Student)\
        .group_by(Student.id, Course.id)\
        .filter(criterion if criterion is not None else true())
    return results

def select_10(criterion = None):
    """Returns courses that teacher reads to student."""
    results = session().query(
        Teacher.first_name,
        Teacher.last_name,
        Course.name,
        Student.first_name,
        Student.last_name
    ).select_from(Score).join(Course).join(Teacher).join(Student)\
        .group_by(Teacher.id, Course.id, Student.id)\
        .filter(criterion if criterion is not None else true())
    return results

def select_11(criterion = None):
    """Returns average score given by a particular teacher to a particular student."""
    results = session().query(
        Teacher.first_name,
        Teacher.last_name,
        Student.first_name,
        Student.last_name,
        func.round(func.avg(Score.score), 2).label('average_score'),
        func.count('*')
    ).select_from(Score).join(Course).join(Teacher).join(Student)\
        .group_by(Teacher.id, Student.id)\
        .filter(criterion if criterion is not None else true())
    return results

def select_12(criterion = None):
    """Returns last lesson's scores for specific course in specific group."""
    # Define the subquery
    subquery = session().query(
        Score.course_id.label('course_id'),
        Student.group_id.label('group_id'),
        func.max(func.cast(Score.datetime, DATE)).label('last_date')
    ).join(Student).group_by(Score.course_id, Student.group_id).subquery()

    results = session().query(
        Course.name,
        Group.name,
        Student.first_name,
        Student.last_name,
        Score.score,
        Score.datetime
    ).select_from(Score)\
    .join(Course, Score.course_id   == Course.id)\
    .join(Student, Score.student_id == Student.id)\
    .join(Group, Student.group_id   == Group.id)\
    .join(subquery,
        and_(
            subquery.c.course_id    == Score.course_id,
            subquery.c.group_id     == Student.group_id,
            subquery.c.last_date    == func.cast(Score.datetime, DATE)  
        )
    )\
    .filter(criterion if criterion is not None else true())\
    .order_by(Student.group_id, Score.course_id)
    return results
