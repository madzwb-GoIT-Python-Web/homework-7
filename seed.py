import datetime
import calendar
import faker
# import pathlib
# import psycopg2
import random
# import tabulate

# import connection
import models

def seed(session):# = connection.session()):
    print("Seeding...")
    # model.metadata.bind = session.bind
    max_students    = 50
    max_teachers    = 5
    # max_courses     = -1
    max_scores      = 20

    _groups = ["A", "B", "C"]
    _courses = [
        "Introduction to Computer Science",
        "Data Structures and Algorithms",
        "Computer Systems Engineering",
        "Introduction to Artificial Intelligence",
        "Operating Systems",
        "Database Management Systems",
        "Software Engineering",
        "Computer Networks",
        "Computer Graphics",
        "Theory of Computation",
        "Machine Learning",
        "Human-Computer Interaction",
        "Computer Security and Cryptography",
        "Distributed Systems",
        "Web Development",
        "Natural Language Processing",
        "Robotics",
        "Computational Biology",
        "Compiler Design",
        "Parallel Computing"
    ]
    _faker = faker.Faker()
    groups  (session, _groups)
    teachers(session, _faker, max_teachers)
    courses (session, _faker, _courses)#, _teachers)
    students(session, _faker, max_students)#,  _groups)
    scores  (session, _faker, max_scores)#, _courses, _students)
    print("Seeding done.")

def groups(session, groups):
    count = 0
    result = ""
    for i, name in enumerate(groups):
        group = models.Group(name=name)#id=i, 
        session.add(group)
        # session.commit()
        # continue
    else:
        try:
            session.commit()
            count = len(groups)
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"with error: {result}." if result else "."
    print(info)

def teachers(session, faker, number):
    count = 0
    result = ""
    datas = []
    for i in range(number):
        first_name  = faker.first_name()
        last_name   = faker.last_name()
        data = (i, first_name, last_name)
        datas.append(data)
        teacher = models.Teacher(first_name=first_name, last_name=last_name)#id=i, 
        session.add(teacher)
    else:
        try:
            session.commit()
            count = number
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"with error: {result}." if result else "."
    print(info)

def courses(session, faker, courses):#, teachers):
    count = 0
    result = ""
    teachers = session.query(models.Teacher).all()
    datas = []
    for i, name in enumerate(courses):
        teacher_id = random.choice(teachers).id
        data = (i, name, teacher_id)
        datas.append(data)
        teacher = models.Course(name=name, teacher_id=teacher_id)#id=i, 
        session.add(teacher)
    else:
        try:
            session.commit()
            count = len(courses)
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"with error: {result}." if result else "."
    print(info)
    
def students(session, faker, number):#, groups):
    count = 0
    result = ""
    groups = session.query(models.Group).all()
    datas = []
    for i in range(number):
        group_id    = random.choice(groups).id
        first_name  = faker.first_name()
        last_name   = faker.last_name()
        # group = random.choice(groups)
        data = (i, first_name, last_name, group_id)#group_i)
        datas.append(data)
        student = models.Student(first_name=first_name, last_name=last_name, group_id=group_id)#id=i, 
        result = session.add(student)
    else:
        try:
            session.commit()
            count = number
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"with error: {result}." if result else "."
    print(info)
    return datas

def scores(session, faker, max_scores):#, courses, students):
    count = 0
    result = ""
    courses = session.query(models.Course).all()
    students = session.query(models.Student).all()
    datas = []
    _calendar = calendar.Calendar(calendar.MONDAY)
    i = 0
    for _ in range(0, max_scores):
        for student in students:
            year    = 2023
            month   = random.randint(1,12)
            days    = []
            for date in _calendar.itermonthdates(year, month):
                if date.month == month and date.weekday() < 5:
                    days.append(date.day)
            # days = calendar.monthrange(year, month)[1]
            # course = random.choices(courses)
            timestamp = datetime.datetime(
                            year,
                            month,
                            random.choice(days),
                            random.randint(9, 21),
                            random.randint(1, 59),
                            random.randint(1, 59)
                        )
            course_id   = random.choice(courses).id
            student_id  = student.id
            timestamp    = timestamp.isoformat()
            score       = random.randint(1, 12)
            data = (i, course_id, student_id, timestamp, score)
            datas.append(data)
            score = models.Score(course_id=course_id, student_id=student_id, datetime=timestamp, score=score)#i=i, 
            session.add(score)
            i += 1
    else:
        try:
            session.commit()
            count = max_scores
        except Exception as e:
            session.rollback()
            result = str(e)
            count = 0
    info = f"{count} record"
    info += "s" if count > 1 else ""
    info += " added"
    info += f"with error: {result}." if result else "."
    print(info)
