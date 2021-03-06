# -*- coding: utf-8 -*-

import os
import json

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.conf import settings

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from quizy.models import (Course, Lesson, LessonEnroll, CourseEnroll)
from quizy.serializers.serializers import (LessonEnrollSerializer, CourseEnrollSerializer)
from quizy.pagination import ListPagination
from quizy.serializers.pupil import PupilSerializer
from quizy.views import validateEmail
from quizy.utils import is_enrolls_different, send_mail

from users.account.models import Account


@api_view(['GET', 'PUT'])
def enroll_teacher(request, enroll_pk):
    """
    возвращает данные назначения для внешнего урока
    для учителя
    сохраняет отзыа от учителя
    """
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if enroll_pk:
        enroll = LessonEnroll.objects.filter(Q(created_by=request.user) | Q(lesson__teacher=request.user) | Q(lesson__course__teacher=request.user), pk=enroll_pk).distinct()
        if enroll:
            enroll = enroll[0]
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        data = json.loads(request.body.decode("utf-8"))
        # enroll.data = normalize(data)
        # проверяем на наличие новых завершенных шагов
        is_equal = is_enrolls_different(enroll.data, data)
        if is_equal is True:
            enroll.required_attention_by_pupil = True
            enroll.success = True
            enroll.data = data
            enroll.data['mode'] = 'wait_pupil'
        else:
            enroll.data = data

        enroll.required_attention_by_teacher = False
        enroll.save()

        if enroll.required_attention_by_pupil is True:

            email_topic = u'English with Experts: Ваш преподаватель проверил Вашу письменную работу.'
            email_from = settings.DEFAULT_FROM_EMAIL
            email_to = [enroll.learner.email]

            email_msg = u'Здравствуйте,\n'
            email_msg += u'Рады сообщить, что Ваш преподаватель проверил Вашу письменную работу. '
            email_msg += u'Чтобы посмотреть Ваши оценки по шкале IELTS и комментарии преподавателя \n'
            email_msg += u'пожалуйста, пройдите по этой ссылке \n(Вам нужно быть зарегистрированым и авторизированым на сайте):\n'
            email_msg += u'http://ieltswriting.englishwithexperts.com/play/' + str(enroll.pk) + '/\n\n'
            email_msg += u'От себя хотим добавить, что IELTS Writing - это самая сложная часть для большинства сдающих (официальная статистика IELTS).'
            email_msg += u'Поэтому не теряйте мотивацию. Чем больше работ Вы напишите до сдачи экзамена, тем лучше. Keep up your good work! Мы верим в Вас!\n\n'
            email_msg += u'Пишите, если у Вас будут вопросы или пожелания к улучшению сервиса. Мы всегда рады конструктивным предложениям.\n\n'
            email_msg += u'Best wishes,\n'
            email_msg += u'English with Experts\n'

            if settings.MAIL is True:
                send_mail(email_topic, email_msg, email_from, email_to)
            elif settings.DEBUG is True:
                print email_topic
                print [enroll.learner.email]
                print email_msg

    enroll = LessonEnrollSerializer(instance=enroll).data
    return Response(enroll, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes((AllowAny, ))
def demo_play(request, lesson_pk=None):
    """
    Тестовый запуск урока в админке редактирования
    """
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    lesson = Lesson.objects.filter(Q(created_by=request.user) | Q(teacher=request.user) | Q(course__teacher=request.user), pk=lesson_pk).distinct()
    if lesson:
        lesson = lesson[0]
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        enroll = LessonEnroll(lesson=lesson, learner=request.user, created_by=request.user)
        enroll = LessonEnrollSerializer(instance=enroll).data
    return Response(enroll, status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
def lesson_picture_upload(request, lesson_pk=None):
    """
    загрузка картинки урока
    """
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    lesson = get_object_or_404(Lesson, pk=lesson_pk, created_by=request.user)
    if request.method == "POST":
        if lesson.picture:
            if os.path.exists(lesson.picture.path):
                os.remove(lesson.picture.path)
                lesson.picture = None

        f = request.FILES.get('file')
        if f and f._size < 30 * 1024 * 1024:
            lesson.picture = f
            lesson.save()

        return Response("OK", status=status.HTTP_200_OK)

    if request.method == "DELETE":
        if lesson.picture:
            if os.path.exists(lesson.picture.path):
                os.remove(lesson.picture.path)
                lesson.picture = None
                lesson.save()
        return Response("OK", status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def pupils(request):
    """
    Запрос на страницы мои ученики
    """
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)
    """
    # проходим по всем назначенным курсам и урока ищем учеников
    dic_pupils = {}

    for ce in CourseEnroll.objects.filter(Q(created_by=request.user) | Q(course__teacher=request.user)):
        dic_pupils.update({
            ce.learner.pk: ce.learner
        })

    for le in LessonEnroll.objects.filter(Q(created_by=request.user) | Q(lesson__teacher=request.user) | Q(lesson__course__teacher=request.user)):
        dic_pupils.update({
            le.learner.pk: le.learner
        })

    pupils = []
    for key, value in dic_pupils.items():
        pupils.append(value)
    """

    paginator = ListPagination()
    result_page = paginator.paginate_queryset(request.user.pupils.all(), request)
    serializer = PupilSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((AllowAny,))
def enroll(request, enroll_pk):
    """
    работа с назначениями со стороны преподователя
    """
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        course_id = data.get('course_id')
        auto_enroll = data.get('auto_enroll')
        lesson_id = data.get('lesson_id')
        email = data.get('email')
        if course_id is None and lesson_id is None:
            return Response("Неверный формат course или lesson", status=status.HTTP_400_BAD_REQUEST)
        if validateEmail(email) is False:
            return Response("Неверный формат email", status=status.HTTP_400_BAD_REQUEST)

        lesson = None
        course = None
        if lesson_id:
            lesson = get_object_or_404(Lesson, pk=lesson_id)
        if course_id:
            course = get_object_or_404(Course, pk=course_id)

        pupil = Account.objects.filter(email__iexact=email)[:1]

        if pupil:
            # проверяем являеться ли ученик учеников преподдователся
            # если нет то назначаем его на преподователя
            exists = request.user.pupils.filter(pk=pupil[0].pk).count()
            if not exists:
                request.user.pupils.add(pupil[0])

        if pupil and lesson:
            try:
                enroll = LessonEnroll.objects.get(lesson=lesson, learner=pupil[0])
            except LessonEnroll.DoesNotExist:
                enroll = LessonEnroll.objects.create(lesson=lesson, learner=pupil[0], created_by=request.user)
                enroll.teachers.add(request.user)

                email_topic = u'English with Experts: Вам назначено письменное задание.'
                email_from = settings.DEFAULT_FROM_EMAIL
                email_to = [pupil[0].email]

                email_msg = u'Здравствуйте,\n'
                email_msg += u'Ваш преподаватель назначила Вам новое задание. '
                email_msg += u'Пожалуйста, пройдите по этой ссылке, чтобы выполнить это задание \n(Вам нужно быть зарегистрированым и авторизированым на сайте):\n'
                email_msg += u'http://ieltswriting.englishwithexperts.com/play/' + str(enroll.pk) + '/\n\n'
                email_msg += u'Пишите, если у Вас будут вопросы. Желаем Вам прогресса в написании работ!\n\n'
                email_msg += u'Best wishes,\n'
                email_msg += u'English with Experts\n'

                if settings.MAIL is True:
                    send_mail(email_topic, email_msg, email_from, email_to)
                elif settings.DEBUG is True:
                    print [pupil[0].email]
                    print email_msg

                # если урок внешний считываем деннаые по умолчанию и сохраняем их в назначение
                if lesson.lesson_type == 'outside':
                    path = os.path.join(settings.BASE_DIR, 'app', 'assets', 'lessons', lesson.path_content)
                    json_path = os.path.join(path, 'default.json')
                    if os.path.exists(json_path):
                        data = json.load(open(json_path))
                        enroll.data = data
                        enroll.save()

            return Response(LessonEnrollSerializer(enroll).data, status=status.HTTP_200_OK)
        elif pupil and course:
            try:
                enroll = CourseEnroll.objects.get(course=course, learner=pupil[0])
            except CourseEnroll.DoesNotExist:
                enroll = CourseEnroll.create(course, pupil[0], request.user)

                if auto_enroll:
                    enroll.auto_enroll = auto_enroll
                    enroll.save()

            return Response(CourseEnrollSerializer(enroll).data, status=status.HTTP_200_OK)
        else:
            return Response({'code': 404}, status=status.HTTP_200_OK)

    if request.method == 'DELETE' and enroll_pk:
        if request.user.is_superuser:
            enroll = LessonEnroll.objects.filter(pk=enroll_pk).distinct()
        else:
            enroll = LessonEnroll.objects.filter(Q(lesson__created_by=request.user) | Q(lesson__teacher=request.user) | Q(lesson__course__teacher=request.user), pk=enroll_pk).distinct()
        if enroll:
            enroll = enroll[0]
            enroll.delete()

        else:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        return Response("", status=status.HTTP_200_OK)

    return Response(status=status.HTTP_200_OK)

