# coding=utf-8
import requests
from BeautifulSoup import BeautifulSoup
from parse import *
from utils import *

# Index to week day name conversion
week_days = {
    0: 'Segunda',
    1: 'Terça',
    2: 'Quarta',
    3: 'Quinta',
    4: 'Sexta',
    5: 'Sábado'
}


def increment_weekday(weekday_skip_counter, current_weekday):
    while True:
        current_weekday = (current_weekday + 1) % 6
        if weekday_skip_counter[current_weekday] == 0:
            break
    return current_weekday


def decrement_weekday_skip_counter(weekday_skip_counter):
    for key in weekday_skip_counter:
        if weekday_skip_counter[key] != 0:
            weekday_skip_counter[key] -= 1
    return weekday_skip_counter


def increment_current_time(current_time):
    current_time.minutes = (current_time.minutes + 30) % 60
    if current_time.minutes == 0:
        current_time.hour += 1


def retrieve_course_name(cookies, faculty, programme):
    url = 'https://sigarra.up.pt/%s/pt/hor_geral.lista_turmas_curso?pv_curso_id=%d' % (faculty, programme)
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text)
    return soup.title.string


def retrieve_programme_classes(cookies, faculty, programme, year, semester):
    url = 'https://sigarra.up.pt/%s/pt/hor_geral.lista_turmas_curso?pv_curso_id=%d&pv_periodos=%d&pv_ano_lectivo=%d' \
          % (faculty, programme, semester, year)
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text)
    years = soup.findAll('table', {'class': 'tabela'})
    ret = []
    for i in years:
        year_ret = {'year': i.find('th').getText()[0]}
        classes_html = i.findAll('a', {'class': 't'})
        classes = []
        for j in classes_html:
            classes.append(
                parse('hor_geral.turmas_view?pv_turma_id={}&pv_periodos=&pv_ano_lectivo=' + str(year), j.get('href'))[
                    0])
        year_ret['classes'] = classes
        ret.append(year_ret)
    return ret


def retrieve_class_timetable(cookies, faculty, class_id, semester, year):
    url = 'https://sigarra.up.pt/%s/pt/hor_geral.turmas_view?pv_turma_id=%d&pv_periodos=%d&pv_ano_lectivo=%d' \
          % (faculty, class_id, semester, year)
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text)
    title = soup.title.string.split(' ')[5]
    timetable = soup.find('table', {'class': 'horario'})
    try:
        rows = [x for x in timetable.contents[2:] if x != '\n']
    except AttributeError:
        return None
    # The current time. It's incremented by half an hour everytime we go to the next row
    current_time = Time(8, 0)
    # When we go to the next row (which means, an extra 30 minutes in the time), we need to account for the fact
    # that the rowspans of the previous classes will make the next rows have less columns. We need to keep track of
    # those classes's duration, so that we can correctly get the week day of the next classes. This dictionary keeps
    # the count for every day of the week.
    weekday_skip_counter = {
        0: 0,
        1: 0,
        2: 0,
        3: 0,
        4: 0,
        5: 0
    }
    # The current weekday. It's incremented every time we move to the next column. Skips the days that have a rowspan
    # from a previous cell, as explained before
    current_weekday = 5

    class_instances = []
    for row in rows:
        classes = [x for x in row.contents[1:] if x != '\n']
        for cell in classes:
            current_weekday = increment_weekday(weekday_skip_counter, current_weekday)
            if cell.getText() != '&nbsp;':
                rowspan = int(cell['rowspan'])
                weekday_skip_counter[current_weekday] = rowspan
                class_type = cell['class']
                course_name = cell.find('acronym')['title']
                acronym = cell.find('a').getText()
                misc = cell.find('table')
                room = misc.find('a').getText()
                start_time = Time(current_time.hour, current_time.minutes)
                end_time = Time(current_time.hour + rowspan / 2, current_time.minutes + (rowspan % 2) * 30)
                course = Course(course_name, acronym)
                class_instance = ClassInstance(title, start_time, end_time, week_days[current_weekday], class_type,
                                               course,
                                               room)
                try:
                    teacher_name = misc.find('acronym')['title']
                    teacher_acronym = misc.find('acronym').getText()
                    teacher_instance = Teacher(teacher_name, teacher_acronym)
                    class_instance.add_teacher(teacher_instance)
                except TypeError:
                    teacher_acronyms = misc.find('td', {'class': 'textod'}).find('a').getText().split('+')
                    for acronym in teacher_acronyms:
                        class_instance.add_teacher(Teacher('-', acronym))
                class_instances.append(class_instance)
        weekday_skip_counter = decrement_weekday_skip_counter(weekday_skip_counter)
        increment_current_time(current_time)
    return class_instances


def get_programmes_from_faculty(cookies, faculty, year):
    url = 'https://sigarra.up.pt/%s/pt/cur_geral.cur_inicio' % faculty
    r = requests.get(url, cookies=cookies)
    soup = BeautifulSoup(r.text)
    data = soup.find('div', {'id': 'ciclos_estudos'})
    data = data.find('div', {'class': 'yui-content'})
    programmes_list_html = data.findAll('ul')
    programmes = []
    for programmes_html in programmes_list_html:
        programmes_temp_html = programmes_html.findAll('li')
        for programme_temp_html in programmes_temp_html:
            programme_info = programme_temp_html.find('a')['href']
            info = parse(
                'cur_geral.cur_view?pv_ano_lectivo=' + str(year) + '&pv_origem=CUR&pv_tipo_cur_sigla={}&pv_curso_id={}',
                programme_info)
            programmes.append((int(info[1]), info[0]))
    return programmes
