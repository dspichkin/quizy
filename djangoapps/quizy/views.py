# -*- coding: utf-8 -*-

import json
import os

# from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q


from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from quizy.models import (Course, Lesson, Page, CourseEnroll, LessonEnroll)
from quizy.serializers.serializers import (CourseEnrollSerializer, LessonEnrollSerializer, LessonSerializer,
PageSerializer)

from quizy.serializers.pupil import PupilSerializer
from quizy.pagination import ListPagination

from users.account.models import Account
from users.account.serializers import UserSerializer, AdminSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
def user_data(request):
    """
    Данные о пользователе
    """
    if not request.user.is_authenticated():
        return Response({'username': 'guest', 'is_authenticated': False})
    if request.user.is_org:
        data = AdminSerializer(request.user).data
    else:
        data = UserSerializer(request.user).data
    data['is_authenticated'] = True
    return Response(data)


def get_user_or_403(request):
    user = request.user
    if not user.is_authenticated():
        raise PermissionDenied()
    return user


def get_enroll(request, course):
    user = get_user_or_403(request)
    enroll = course.enrolls.get(learner=user)
    return enroll


def validateEmail(email):
    from django.core.validators import validate_email
    from django.core.exceptions import ValidationError
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


@api_view(['GET'])
def lesson(request, lesson_pk=None):
    if lesson_pk is None:
        lesson = Lesson.objects.all(created_by=request.user)
    else:
        lesson = get_object_or_404(Lesson, pk=lesson_pk)
    enroll = get_enroll(request, lesson)
    data = LessonEnrollSerializer(enroll).data
    data.update(LessonSerializer(lesson).data)
    return Response(data)


@api_view(['GET', 'PUT'])
@permission_classes((AllowAny, ))
def demo_play(request, lesson_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    try:
        lesson = Lesson.objects.get(Q(created_by=request.user) | Q(teacher=request.user) | Q(course__teacher=request.user), pk=lesson_pk,)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        # if lesson.created_by == request.user or :
        enroll = LessonEnroll(lesson=lesson, learner=request.user, created_by=request.user)

    return Response(LessonEnrollSerializer(instance=enroll).data, status=status.HTTP_200_OK)


@api_view(['POST'])
def new_page(request, lesson_pk=None):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    lesson = get_object_or_404(Lesson, pk=lesson_pk, created_by=request.user)
    if request.method == "POST":
        if request.body:
            req = json.loads(request.body.decode("utf-8"))

            if type(req) is dict:
                text = req.get("text")
                type_page = req.get("type")
                number = req.get("number")

                page = Page.objects.create(text=text, type=type_page, number=number, lesson=lesson)
                raw_variants = req.get("variants", [])
                for v in raw_variants:
                    text = v.get("text")
                    right_answer = v.get("right_answer")
                    page.variants.create(text=text, right_answer=right_answer)
                serializer = PageSerializer(instance=page)
                return Response(serializer.data)
            # сохраняем только номера
            if type(req) is list:
                is_dirty = False
                for q in req:
                    id = q.get('id')
                    if id:
                        page, created = Page.objects.get_or_create(pk=id, lesson=lesson)
                        if page.number != q.get('number'):
                            page.number = int(q.get('number'))
                            is_dirty = True
                        if is_dirty is True:
                            page.save()
                return Response("OK", status=status.HTTP_200_OK)


@api_view(['POST', 'DELETE'])
def lesson_picture_upload(request, lesson_pk=None):
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


@api_view(['POST', 'DELETE'])
def page_picture_upload(request, page_pk=None):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    page = get_object_or_404(Page, pk=page_pk)
    if page.lesson.created_by != request.user:
        return Response("OK", status=status.HTTP_200_OK)

    if request.method == "POST":
        if page.media:
            if os.path.exists(page.media.path):
                os.remove(page.media.path)
                page.media = None

        f = request.FILES.get('file')
        if f and f._size < 30 * 1024 * 1024:
            page.media = f
            page.save()

        return Response("OK", status=status.HTTP_200_OK)

    if request.method == "DELETE":
        if page.media:
            if os.path.exists(page.media.path):
                os.remove(page.media.path)
                page.media = None
                page.save()
        return Response("OK", status=status.HTTP_200_OK)

"""
@api_view(['GET', 'POST'])
@permission_classes((AllowAny,))
def lesson_archive(request, lesson_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if request.method == 'GET' and lesson_pk is None:

        lessonEnrolls = LessonEnroll.objects.filter(learner=request.user,
            is_archive=True)
        archives = []
        for a in lessonEnrolls:
            archives.append(LessonEnrollSerializer(instance=a).data)
        return Response(archives, status=status.HTTP_200_OK)

    if request.method == 'POST' and lesson_pk is not None:
        lessonEnrolls = LessonEnroll.objects.filter(lesson=lesson_pk, learner=request.user,
            is_archive=False)

        if len(lessonEnrolls) > 0:
            lessonEnroll = lessonEnrolls[0]
            lessonEnroll.is_archive = True
            lessonEnroll.date_archive = timezone.now()
            lessonEnroll.save()
            return Response(LessonEnrollSerializer(instance=lessonEnroll).data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
"""

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_mypupil(request):
    """
    запрос для получения адресов
    используеться при назначение
    """
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    attr_email = request.GET.get('email')
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
        if attr_email is not None:
            if attr_email in value.email:
                pupils.append(value.email)
        else:
            pupils.append(value.email)

    return Response(pupils, status=status.HTTP_200_OK)


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
        # pupils.append(PupilSerializer(value).data)

    paginator = ListPagination()
    result_page = paginator.paginate_queryset(pupils, request)
    serializer = PupilSerializer(result_page, many=True)
    return paginator.get_paginated_response(serializer.data)

    # return Response(pupils, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def create_pupil(request):

    if not request.user.is_authenticated():
        return Response(status=status.HTTP_200_OK)

    data = json.loads(request.body.decode("utf-8"))
    lesson_id = data.get('lesson_id')
    email = data.get('email')
    if validateEmail(email) is False:
        return Response("Неверный формат email", status=status.HTTP_400_BAD_REQUEST)

    lesson = get_object_or_404(Lesson, pk=lesson_id, created_by=request.user)
    pupil, created = Account.objects.get_or_create(email__iexact=email)
    if created:
        pupil.email = email
        pupil.username = email
        pupil.account_type = 2
        pupil.save()

    try:
        LessonEnroll.objects.get(lesson=lesson, learner=pupil)
    except LessonEnroll.DoesNotExist:
        LessonEnroll.objects.create(lesson=lesson, learner=pupil, created_by=request.user)

    request.user.pupils.add(pupil)
    return Response(UserSerializer(pupil).data, status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((AllowAny,))
def enroll_pupil(request, enroll_pk):
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


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((AllowAny,))
def enroll_course_pupil(request, enroll_pk):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_200_OK)

    if request.method == 'DELETE' and enroll_pk:
        try:
            enroll = CourseEnroll.objects.get(Q(created_by=request.user) | Q(course__teacher=request.user), pk=enroll_pk)
            enroll.delete()
        except CourseEnroll.DoesNotExist:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        return Response("", status=status.HTTP_200_OK)

    return Response(status=status.HTTP_200_OK)


