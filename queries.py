import tabulate
from sqlalchemy import and_, text

import argparser as ap
import models
import my_select
import registrator.registrator as registrator

def select(function, criterion = None):
    print(function.__name__)
    results = function(criterion)
    print(function.__doc__)
    print(
        tabulate.tabulate(
            results,
            headers =[column["name"] for column in results.column_descriptions],
            tablefmt="grid",
            floatfmt=".2f"
        )
    )
    print()

def select_01(args):#, **kwargs):
    criterion = None
    query = my_select.select_01()
    select(my_select.select_01, criterion)
    
def select_02(args):#, **kwargs):
    criterion = models.Course.id == 1
    # criterion = None
    query = my_select.select_02()
    select(my_select.select_02, criterion)

def select_03(args):#, **kwargs):
    criterion = models.Course.id == 1
    # criterion = text("courses.id = 1")
    # criterion = None
    select(my_select.select_03, criterion)

def select_04(args):#, **kwargs):
    criterion = None
    select(my_select.select_04, criterion)

def select_05(args):#, **kwargs):
    criterion = models.Teacher.id == 1
    select(my_select.select_05, criterion)

def select_06(*rgs):#, **kwargs):
    criterion = models.Group.id == 1
    # criterion = None
    select(my_select.select_06, criterion)

def select_07(args):#, **kwargs):
    criterion = and_(models.Course.id == 1, models.Group.id == 1)
    # criterion = None
    select(my_select.select_07, criterion)
    
def select_08(args):#, **kwargs):
    criterion = models.Teacher.id == 1
    # criterion = None
    select(my_select.select_08, criterion)

def select_09(*args):#, **kwargs):
    criterion = models.Student.id == 1
    # criterion = None
    select(my_select.select_09, criterion)

def select_10(args):#, **kwargs):
    criterion = and_(models.Teacher.id == 1, models.Student.id == 1)
    # criterion = None
    select(my_select.select_10, criterion)

def select_11(args):#, **kwargs):
    criterion = and_(models.Teacher.id == 1, models.Student.id == 1)
    # criterion = None
    select(my_select.select_11, criterion)

def select_12(args):#, **kwargs):
    criterion = and_(models.Score.course_id == 1, models.Student.group_id == 1)
    # criterion = model.Score.course_id == 0
    # criterion = model.Student.group_id == 0
    # criterion = None
    select(my_select.select_12, criterion)


class QUERIES(registrator.REGISTRATOR):    ...
QUERIES.register("select_", __name__, globals(), type(select) ,["__builtins__",], False)
registry = QUERIES()
