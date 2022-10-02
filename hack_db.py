from django.core.exceptions import ObjectDoesNotExist
from datacenter.models import *


def fix_marks(schoolkid_name, make_mark=5):

    if not schoolkid_name:
        print('Не введено ФИО ученика! Введите ФИО')

    try:
        schoolkid = Schoolkid.objects.get(full_name=schoolkid_name)

        all_bad_marks = Mark.objects.filter(schoolkid=schoolkid.pk).filter(points__lt=4)

        for mark in all_bad_marks:
            mark.points = make_mark
            mark.save()

        print(f'У ученика {schoolkid_name} все плохие оценки заменены на {make_mark}!')

    except ObjectDoesNotExist:
        print(f'К сожалению, не нашли такого ученика: {schoolkid_name}. Возможно опечатка.')


def remove_chastisements(schoolkid_name):

    if not schoolkid_name:
        print('Не введено ФИО ученика! Введите ФИО')

    try:
        schoolkid = Schoolkid.objects.get(full_name=schoolkid_name)
        all_chastisements = Chastisement.objects.filter(schoolkid=schoolkid)
        all_chastisements.delete()

        print(f'У ученика {schoolkid_name} удалены все замечания!')

    except ObjectDoesNotExist:
        print(f'К сожалению, не нашли такого ученика: {schoolkid_name}. Возможно опечатка.')


def create_recommendation(schoolkid_name, lesson_name, text='Хвалю'):

    if not schoolkid_name:
        print('Не введено ФИО ученика! Введите ФИО')

    try:
        schoolkid = Schoolkid.objects.get(full_name=schoolkid_name)

        lesson = Lesson.objects.filter(
            subject__title=lesson_name,
            year_of_study=schoolkid.year_of_study,
            group_letter=schoolkid.group_letter,
        ).last()
        chastisement = Chastisement.objects.create(text=text, schoolkid=schoolkid,
                                                   subject=lesson.subject, teacher=lesson.teacher,
                                                   created=lesson.date)

        print(f'У ученика {schoolkid_name} добавлено замечание {text} к последнему уроку {lesson_name}!')

    except ObjectDoesNotExist:
        print(f'К сожалению, не нашли такого ученика: {schoolkid_name}. Возможно опечатка.')
