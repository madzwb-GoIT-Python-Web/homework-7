import tabulate
from sqlalchemy import and_, text, any_

import argparser as ap
import commands
import models
import my_select
import registrator.registrator as registrator

def select(function, criterion: bool|None = None):
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

def select_01(args):
    criterion = None
    query = my_select.select_01()
    select(my_select.select_01, criterion)
    
def select_02(args):
    columns = [models.Course.id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = models.Course.id == filters[0]["id"]
    else:
        criterion = False
    select(my_select.select_02, criterion)

def select_03(args):
    columns = [models.Course.id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = models.Course.id == filters[0]["id"]
    else:
        criterion = False
    select(my_select.select_03, criterion)

def select_04(args):
    criterion = None
    select(my_select.select_04, criterion)

def select_05(args):
    columns = [models.Teacher.id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = models.Teacher.id == filters[0]["id"]
    else:
        criterion = models.Teacher.id == 1
    select(my_select.select_05, criterion)

def select_06(args):
    columns = [models.Group.id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = models.Group.id == filters[0]["id"]
    else:
        criterion = False
    select(my_select.select_06, criterion)

def select_07(args):
    columns = [models.Course.id, models.Group.id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = and_(
                        models.Course.id == filters[0]["id"],
                        models.Group.id == filters[0]["id"]
                    )
    else:
        criterion = False
    select(my_select.select_07, criterion)
    
def select_08(args):
    columns = [models.Teacher.id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = models.Teacher.id == filters[0]["id"]
    else:
        criterion = False
    select(my_select.select_08, criterion)

def select_09(args):
    columns = [models.Teacher.id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = models.Student.id == filters[0]["id"]
    else:
        criterion = False
    select(my_select.select_09, criterion)

def select_10(args):
    columns = [models.Teacher.id, models.Student.id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = and_(
                        models.Teacher.id == filters[0]["id"],
                        models.Student.id == filters[0]["id"]
                    )
    else:
        criterion = False
    select(my_select.select_10, criterion)

def select_11(args):
    columns = [models.Teacher.id, models.Student.id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = and_(
                        models.Teacher.id == filters[0]["id"],
                        models.Student.id == filters[0]["id"]
                    )
    else:
        criterion = False
    select(my_select.select_11, criterion)

def select_12(args):
    columns = [models.Score.course_id, models.Student.group_id]
    filters = commands.__parse_args(args.filter, columns)
    if filters:
        criterion = and_(
                        models.Score.course_id == filters[0]["course_id"],
                        models.Student.group_id == filters[0]["group_id"]
                    )
    else:
        criterion = False
    select(my_select.select_12, criterion)

class QUERIES(registrator.REGISTRATOR):    ...
QUERIES.register("select_", __name__, globals(), type(select) ,["__builtins__",], False)
registry = QUERIES()
