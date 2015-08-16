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
from quizy.utils import normalize

from users.account.models import Account


@api_view(['GET', 'PUT'])
def enroll_teacher(request, enroll_pk):
    """
    возвращает данные назначения для внешнего урока
    для учителя
    """
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if enroll_pk:
        try:
            enroll = LessonEnroll.objects.get(Q(created_by=request.user) | Q(lesson__teacher=request.user) | Q(lesson__course__teacher=request.user), pk=enroll_pk)
        except LessonEnroll.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        data = json.loads(request.body.decode("utf-8"))
        enroll.data = normalize(data)
        enroll.required_attention_by_teacher = False
        enroll.required_attention_by_pupil = True

        enroll.success = True
        enroll.save()

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

    try:
        lesson = Lesson.objects.get(Q(created_by=request.user) | Q(teacher=request.user) | Q(course__teacher=request.user), pk=lesson_pk,)
    except Lesson.DoesNotExist:
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

    paginator = ListPagination()
    result_page = paginator.paginate_queryset(pupils, request)
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

        if pupil and lesson:
            try:
                enroll = LessonEnroll.objects.get(lesson=lesson, learner=pupil[0])
            except LessonEnroll.DoesNotExist:
                enroll = LessonEnroll.objects.create(lesson=lesson, learner=pupil[0], created_by=request.user)

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
        try:
            enroll = LessonEnroll.objects.get(Q(lesson__created_by=request.user) | Q(lesson__teacher=request.user) | Q(lesson__course__teacher=request.user), pk=enroll_pk)
            enroll.delete()
        except LessonEnroll.DoesNotExist:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        return Response("", status=status.HTTP_200_OK)

    return Response(status=status.HTTP_200_OK)

