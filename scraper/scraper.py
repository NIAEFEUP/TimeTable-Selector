# coding=utf-8
from exporter import export_data
from processer import process_courses, get_teachers_without_names
from retriever import *
import requests
import sys

# Put the faculties you wish to extract data from here. Put them just like they appear in sigarra's page.
faculties = ['fadeup']


def login():
    url = 'https://sigarra.up.pt/feup/pt/vld_validacao.validacao'

    login_data = {
        'p_user': user,
        'p_pass': password,
        'p_app': 162,
        'p_amo': 1721,
        'p_address': 'WEB_PAGE.INICIAL'
    }

    r = requests.post(url, data=login_data)
    return r.cookies


def main():
    cookies = login()
    programmes = {}

    print 'Retrieving programmes from the faculties'
    for faculty in range(len(faculties)):
        programmes[faculties[faculty]] = get_programmes_from_faculty(cookies, faculties[faculty], year)
    print 'Retrieving courses... Please wait...'
    j = 1
    for faculty in programmes:
        data = []
        programmes_classes = []
        print '\tRetrieving faculty ' + str(j) + '/' + str(len(programmes)) + ' (' + faculty + '). Please wait...'
        i = 1
        for programme in programmes[faculty]:
            programme_classes = {'name': retrieve_course_name(cookies, faculty, programme[0]),
                                 'classes': retrieve_programme_classes(cookies, faculty, programme[0], year, semester),
                                 'type': programme[1]}
            programmes_classes.append(programme_classes)
            print '\t\tCourse ' + str(i) + '/' + str(len(programmes[faculty])) + ' complete.'
            i += 1

        print '\n\tRetrieving classes from each programme... Please wait...'
        for programme in range(len(programmes_classes)):
            programme_instance = Programme(programmes_classes[programme]['name'], programmes_classes[programme]['type'])
            print '\t\tRetrieving programme ' + str(programme+1) + '/' + str(len(programmes_classes)) + ' (' +\
                  programmes_classes[programme]['name'] + '). Please wait...'
            for timetables in programmes_classes[programme]['classes']:
                courses = []
                for timetable in timetables['classes']:
                    timetable_instance = retrieve_class_timetable(cookies, faculty, int(timetable), semester, year)
                    if timetable_instance is None:
                        continue
                    courses = process_courses(courses, timetable_instance)
                programme_instance.add_school_year(Year(timetables['year'], courses))
                print '\t\t\tSchool year ' + str(timetables['year']) + ' complete.'
            data.append(programme_instance)

        get_teachers_without_names(data)
        print '\nExporting the data to JSON files... Please wait...'
        export_data(faculty, data)
        j += 1


if len(sys.argv) != 5:
    print 'Usage: python scraper.py [username] [password] [year] [semester]'
    print 'Example: python scraper.py up201301234 12345 2016 1'
else:
    user = sys.argv[1]
    password = sys.argv[2]
    year = int(sys.argv[3])
    semester = int(sys.argv[4])
    main()
