# coding=utf-8

from utils import Course, Class, Lesson


def course_index_in_list(courses, course_acronym):
    course = 0
    while course < len(courses) and courses[course].acronym <= course_acronym:
        if courses[course].acronym == course_acronym:
            return course
        course += 1
    return -1


def class_index_in_course(classes, class_name):
    cl = 0
    while cl < len(classes):
        if classes[cl].name == class_name:
            return cl
        cl += 1
    return -1


def process_courses(courses, timetable):
    for class_instance in timetable:
        if len(courses) != 0:
            index = course_index_in_list(courses, class_instance.course.acronym)
        else:
            index = -1
        if index == -1:
            course = Course(class_instance.course.name, class_instance.course.acronym)
            index_class = class_index_in_course(course.classes, class_instance.name)
            if index_class == -1:
                new_class = Class(class_instance.name)
                new_class.add_lesson(Lesson(class_instance.start_time, class_instance.end_time,
                                            class_instance.week_day, class_instance.class_type, class_instance.room,
                                            class_instance.teachers))
                course.add_class(new_class)
            else:
                course.classes[index_class].add_lesson(Lesson(class_instance.start_time, class_instance.end_time,
                                                              class_instance.week_day, class_instance.class_type,
                                                              class_instance.room,
                                                              class_instance.teachers))
            courses.append(course)
            courses.sort(key=lambda x: x.acronym)
        else:
            index_class = class_index_in_course(courses[index].classes, class_instance.name)
            if index_class == -1:
                new_class = Class(class_instance.name)
                new_class.add_lesson(Lesson(class_instance.start_time, class_instance.end_time,
                                            class_instance.week_day, class_instance.class_type, class_instance.room,
                                            class_instance.teachers))
                courses[index].add_class(new_class)
            else:
                courses[index].classes[index_class].add_lesson(
                    Lesson(class_instance.start_time, class_instance.end_time,
                           class_instance.week_day, class_instance.class_type,
                           class_instance.room,
                           class_instance.teachers))

    return courses


def get_teachers_without_names(data):
    for programme in data:
        for year in programme.school_years:
            for course in year.courses:
                for class_instance in course.classes:
                    for lesson in class_instance.lessons:
                        for teacher in lesson.teachers:
                            if teacher.name == '-':
                                name = get_teacher_name_from_programme(programme, teacher.acronym)
                                if name == '-':
                                    name = get_teacher_name_from_faculty(data, teacher.acronym)
                                teacher.name = name


def get_teacher_name_from_programme(programme, acronym):
    for year in programme.school_years:
        for course in year.courses:
            for class_instance in course.classes:
                for lesson in class_instance.lessons:
                    for teacher in lesson.teachers:
                        if teacher.acronym == acronym:
                            return teacher.name

    return '-'


def get_teacher_name_from_faculty(data, acronym):
    for programme in data:
        name = get_teacher_name_from_programme(programme, acronym)
        if name != '-':
            return name
    return '-'
