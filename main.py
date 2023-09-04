# from sqlalchemy import MetaData, Table, Column, Integer, String, DateTime, ForeignKey, and_, or_

import argparser as ap
import connection
# import models
# import queries
import seed
# import tabulate
# import my_select

def main():
    ap.create_parser()
    args = ap.parser.parse_args()

    connection.connect(args)
    try:
        open(".lock","r")
    except Exception as e:
        # Switched to use alembic
        # model.Base.metadata.drop_all(connection.session().bind)
        # connection.session().commit()
        # model.Base.metadata.create_all(connection.session().bind)
        seed.seed(connection.session())
        open(".lock","w")
    while True:
        command = input(">")
        commands = ap.parse_command(command)
        parsed_commands = ap.parse_commands(commands)
        # exit
        if parsed_commands:
            if ap.check_exit(parsed_commands.command):
                break
    # for name, query in queries.registry.items():
    #     query()
    return



# def core(engine = None):
#     metadata = MetaData()

#     groups      = Table(
#                     "groups", metadata,
#                     Column("id"         , Integer, primary_key = True),
#                     Column("name"       , String),
#                 )

#     students    = Table(
#                     "students", metadata,
#                     Column("id"         , Integer, primary_key = True),
#                     Column("group_id"   , Integer, ForeignKey('groups.id')),
#                     Column("first_name" , String),
#                     Column("last_name"  , String),
#                 )
    
#     teachers    = Table(
#                     "teachers", metadata,
#                     Column("id"         , Integer, primary_key = True),
#                     Column("first_name" , String),
#                     Column("last_name"  , String),
#                 )

#     courses     = Table(
#                     "courses", metadata,
#                     Column("id"         , Integer, primary_key = True),
#                     Column("teacher_id" , Integer, ForeignKey('teachers.id')),
#                     Column("name"       , String),
#                 )

#     scores      = Table(
#                     "scores", metadata,
#                     Column("id"         , Integer, primary_key = True),
#                     Column("course_id"  , Integer, ForeignKey('courses.id')),
#                     Column("student_id" , Integer, ForeignKey('students.id')),
#                     Column("datetime"   , DateTime),
#                     Column("score"      , Integer),
#                 )
#     if engine is not None:
#         metadata.create_all(engine)
#     return groups, students, teachers, courses, scores

if __name__ == "__main__":
    main()