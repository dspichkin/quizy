# -*- coding: utf-8 -*-

import json
import os

# from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.conf import settings

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from quizy.models import (Lesson, Page, CourseEnroll, LessonEnroll, Statistic, Tag)
from quizy.serializers.serializers import (LessonEnrollSerializer, LessonSerializer,
PageSerializer, StatisticSerializer, LessonForEnrollSerializer, TagSerializer)

# from quizy.serializers.pupil import PupilSerializer
from quizy.pagination import (ListPagination, LessonPagination)
from quizy.utils import send_mail

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


@api_view(['POST'])
def new_page(request, lesson_pk=None):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_400_BAD_REQUEST)
    lesson = Lesson.objects.filter(Q(created_by=request.user) | Q(teacher=request.user) | Q(course__teacher=request.user), pk=lesson_pk).distinct()
    if lesson:
        lesson = lesson[0]
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
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
def page_picture_upload(request, page_pk=None):
    """
    загрузка медия для вопроса
    """
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_400_BAD_REQUEST)

    page = get_object_or_404(Page, pk=page_pk)
    lesson = Lesson.objects.filter(Q(created_by=request.user) | Q(teacher=request.user) | Q(course__teacher=request.user), pk=page.lesson.pk).distinct()
    if len(lesson) == 0:
        return Response("PermissionDenied", status=status.HTTP_200_OK)

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


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_mypupil(request):
    """
    запрос для получения адресов учеников
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
    email_msg = "dic_pupils %s" % request.user.pupils.all()

    # так же берем из моих учеников
    for p in request.user.pupils.all():
        dic_pupils.update({
            p.pk: p
        })

    email_topic = u'test'
    email_from = settings.DEFAULT_FROM_EMAIL
    email_to = ['user783@gmail.com']
    
    email_msg += "request.user.pupils.all() %s" % request.user.pupils.all()
    send_mail(email_topic, email_msg, email_from, email_to)

    pupils = []
    for key, value in dic_pupils.items():
        if attr_email is not None:
            if attr_email in value.email:
                pupils.append(value.email)
        else:
            pupils.append(value.email)

    return Response(pupils, status=status.HTTP_200_OK)


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
def enroll_course_pupil(request, enroll_pk):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_200_OK)

    if request.method == 'DELETE' and enroll_pk:
        enroll = CourseEnroll.objects.filter(Q(created_by=request.user) | Q(course__teacher=request.user), pk=enroll_pk).distinct()
        if enroll:
            enroll = enroll[0]
            enroll.delete()
        else:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        return Response("", status=status.HTTP_200_OK)

    return Response(status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE'])
@permission_classes((AllowAny,))
def statistic(request, statistic_pk):
    """
    Запрос на статтистику по ученикам
    """
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)
    pupils = Statistic.objects.filter(Q(lesson__teacher=request.user) | Q(lesson__course__teacher=request.user))

    if request.method == "GET":
        dic_pupils = {}
        for p in pupils:
            if (p.learner.id in dic_pupils):
                enrolls = dic_pupils[p.learner.id].get('enrolls', [])
                enrolls.append(StatisticSerializer(p).data)
                dic_pupils[p.learner.id]['enrolls'] = enrolls
            else:
                dic_pupils[p.learner.id] = {
                    'learner': UserSerializer(p.learner).data,
                    'enrolls': [StatisticSerializer(p).data]
                }
        a = []
        for key, value in dic_pupils.items():
            a.append(value)
        paginator = ListPagination()
        result_page = paginator.paginate_queryset(a, request)

        return paginator.get_paginated_response(result_page)

    if request.method == "DELETE" and statistic_pk:
        try:
            s = Statistic.objects.filter(Q(lesson__teacher=request.user) | Q(lesson__course__teacher=request.user), pk=statistic_pk).distinct()
            s.delete()
        except Statistic.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response("OK", status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_last_lessons(request, tag_slug):
    """
    возвращет последние шесть урокоа для главной страницы
    """
    if request.method == "GET":
        if tag_slug:
            slug = Tag.objects.filter(slug=tag_slug)
            lessons = Lesson.objects.filter(full_lesson_type=2, is_public=True, is_active=True, tag__in=slug).order_by('-updated_at')
        else:
            lessons = Lesson.objects.filter(full_lesson_type=2, is_public=True, is_active=True).order_by('-updated_at')
        data_lessons = LessonForEnrollSerializer(lessons, many=True).data
        paginator = LessonPagination()
        result_page = paginator.paginate_queryset(data_lessons, request)
        return paginator.get_paginated_response(result_page)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_tags(request):
    """
    возвращет последние шесть урокоа для главной страницы
    """
    if request.method == "GET":
        tags = Tag.objects.all().order_by('-name')
        return Response(TagSerializer(tags, many=True).data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_avatar(request):
    """
    возвращет аватар
    """
    if request.method == "GET":
        print request.GET
        email = request.GET.get('email').decode("utf-8")
        if email:
            try:
                user = Account.objects.get(email=email)
            except Account.DoesNotExist:
                return Response("OK", status=status.HTTP_200_OK)
            if user:
                data = UserSerializer(user).data
                return Response(data.get('thumbnail_avatar'), status=status.HTTP_200_OK)
        return Response("OK", status=status.HTTP_200_OK)



