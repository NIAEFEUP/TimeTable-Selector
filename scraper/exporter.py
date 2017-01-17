# coding=utf-8
import json
import os


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        else:
            return json.JSONEncoder.default(self, o)


def export_data(faculty, data):
    if not os.path.exists('data' + os.path.sep + faculty):
        os.makedirs('data' + os.path.sep + faculty)
    for programme in data:
        for char in '\\/:*?"<>|':
            programme.name = programme.name.replace(char, '')
        if not os.path.exists('data' + os.path.sep + faculty + os.path.sep + programme.type):
            os.makedirs('data' + os.path.sep + faculty + os.path.sep + programme.type)
        if not os.path.exists('data' + os.path.sep + faculty + os.path.sep + programme.type + os.path.sep + programme.name):
            os.makedirs('data' + os.path.sep + faculty + os.path.sep + programme.type + os.path.sep + programme.name)
        for year in programme.school_years:
            if not os.path.exists('data' + os.path.sep + faculty + os.path.sep + programme.type + os.path.sep + programme.name + os.path.sep +
                                          str(year.number)):

                os.makedirs('data' + os.path.sep + faculty + os.path.sep + programme.type + os.path.sep + programme.name + os.path.sep + str(
                    year.number))
            for course in year.courses:
                s = json.dumps(course.to_json(), cls=JSONEncoder)
                with open('data' + os.path.sep + faculty + os.path.sep + programme.type + os.path.sep + programme.name + os.path.sep + str(
                        year.number) + os.path.sep + course.acronym + '.json', 'w') as f:
                    f.write(s)
