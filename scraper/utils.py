# coding=utf-8


class Faculty:
    def __init__(self, acronym, programmes):
        self.acronym = acronym
        self.programmes = programmes


class Programme:
    def __init__(self, name, course_type):
        self.name = name
        self.type = course_type
        self.school_years = []

    def add_school_year(self, year):
        self.school_years.append(year)


class Year:
    def __init__(self, number, courses):
        self.number = number
        self.courses = courses


class Course:
    def __init__(self, name, acronym):
        self.name = name
        self.acronym = acronym
        self.classes = []

    def add_class(self, class_instance):
        self.classes.append(class_instance)

    def to_json(self):
        return dict(name=self.name, acronym=self.acronym, classes=self.classes)


class Class:
    def __init__(self, name):
        self.name = name
        self.lessons = []

    def add_lesson(self, lesson):
        self.lessons.append(lesson)

    def to_json(self):
        return dict(name=self.name, lessons=self.lessons)


class Lesson:
    def __init__(self, start_time, end_time, week_day, class_type, room, teachers):
        self.start_time = start_time
        self.end_time = end_time
        self.week_day = week_day
        self.class_type = class_type
        self.room = room
        self.teachers = teachers

    def to_json(self):
        return dict(start_time=self.start_time, end_time=self.end_time, week_day=self.week_day,
                    class_type=self.class_type, room=self.room, teachers=self.teachers)


class Teacher:
    def __init__(self, name, acronym):
        self.name = name
        self.acronym = acronym

    def to_json(self):
        return dict(name=self.name, acronym=self.acronym)


class Time:
    def __init__(self, hour, minutes):
        self.hour = hour
        self.minutes = minutes

    def earlier_than(self, date):
        if self.hour == date.hour and self.minutes == date.minutes:
            return False
        else:
            return not self.later_than(date)

    def later_than(self, date):
        if self.hour > date.hour:
            return True
        elif self.hour < date.hour:
            return False
        if self.minutes > date.minutes:
            return True
        else:
            return False

    def to_json(self):
        return dict(hour=self.hour, minutes=self.minutes)


# The following classes are only used in the retrieving phase

class ClassInstance:
    def __init__(self, name, start_time, end_time, week_day, class_type, course, room):
        self.name = name
        self.start_time = start_time
        self.end_time = end_time
        self.week_day = week_day
        self.class_type = class_type
        self.course = course
        self.room = room
        self.teachers = []

    def add_teacher(self, teacher):
        self.teachers.append(teacher)


class ClassCourse:
    def __init__(self, name, acronym):
        self.name = name
        self.acronym = acronym

