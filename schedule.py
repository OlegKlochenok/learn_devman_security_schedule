import argparse
import datetime
import locale
from docxtpl import DocxTemplate

locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')

objects_security = ['ГСМ', 'Стоянка', 'Ангар']


def get_data_work_shift(defolt_count, defolt_new_object, defolt_dead_object):
    parser = argparse.ArgumentParser(
        description=
        """
        Получить файл с расписанием на текущую смену можно командой
        `python3 main.py`.
        
        Если Вам нужно сформировать расписание на несколько смен,
        не только на текущую, укажите требуемое количество смен
        в команде запуска:
        `python3 main.py -с <количество смен>`.
        Например: `python3 main.py -с 5`
        
        Если Вам нужно добавить новый объект охраны в рассчёт:
        `python3 main.py -o <название объекта>`
        Например: `python3 main.py -o Гараж`
        
        Если Вам нужно добавить несколько новых объектов охраны
        в рассчёт:
        `python3 main.py -oo <"название объекта, название объекта">`
        Например: `python3 main.py -d Пляж`

        """
    )
    parser.add_argument('-c', '--count',
                        default=defolt_count,
                        help='укажите количество рассчитываемых смен в команде '
                             'запуска: `python3 main.py -с <количество смен>`.',
                        type=int)
    parser.add_argument('-o', '--object',
                        default=defolt_new_object,
                        help='укажите новый объект в команде запуска: '
                             '`python3 main.py -o <название объекта>`.',
                        type=str)
    parser.add_argument('-oo', '--objects',
                        default=defolt_dead_object,
                        help='укажите новые объекты '
                             'в команде запуска: `python3 main.py -d <"название объекта, название объекта">`.',
                        type=str)
    args = parser.parse_args()

    return args.count, args.object, args.objects


count_work_shift, new_object, news_objects = get_data_work_shift(1, '', '')

start_day = datetime.datetime.today()
start_first_shift = start_day.combine(start_day.date(), datetime.time(8, 0))
end_last_shift = start_first_shift + datetime.timedelta(hours=count_work_shift * 24)

if new_object:
    objects_security.append(new_object)

if news_objects:
    list_news_objects = news_objects.split(', ')
    objects_security.extend(list_news_objects)


def print_data():
    print(start_day)
    print(start_first_shift)
    print(end_last_shift)


schedule = DocxTemplate("template.docx")
context = {
    'start_day': start_first_shift.strftime('%d.%m.%Y'),
    'end_day': end_last_shift.strftime('%d.%m.%Y'),
}
schedule.render(context)
schedule.save(f"{start_first_shift.strftime('%d%m%Y')}-{end_last_shift.strftime('%d%m%Y')}.docx")
