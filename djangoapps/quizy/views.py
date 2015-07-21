# -*- coding: utf-8 -*-

import json
import os
import re

# from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from sorl.thumbnail import get_thumbnail

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from quizy.models import Lesson, Page, Variant, LessonEnroll
from quizy.serializers import (EnrollSerializer, LessonSerializer,
PageSerializer, VariantSerializer)

from users.account.models import Account
from users.account.serializers import UserSerializer, AdminSerializer
# class HomePageView(TemplateView):
#    template_name = 'index.html'


class PageViewSet(viewsets.ModelViewSet):
    serializer_class = PageSerializer
    model = Page
    lookup_field = 'id'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    queryset = Page.objects.all()

    """
    def put(self, request, *args, **kwargs):

        data = request.DATA
        serializer = pageSerializer(data=data, many=True)

        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    """
    def update(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        if not pk:
            res = {"code": 400, "message": "Bad Requset"}
            return Response(json.dumps(res), status=status.HTTP_200_OK)

        if request.method == "PUT":
            req = json.loads(request.body.decode("utf-8"))
            is_dirty = False
            text = req.get("text")
            type = req.get("type")
            number = req.get("number")
            page = Page.objects.get(pk=pk)
            if page.text != text:
                page.text = text
                is_dirty = True
            if page.type != type:
                page.type = type
                is_dirty = True
            if page.number != number:
                page.number = number
                is_dirty = True
            if is_dirty is True:
                page.save()

            raw_variants = req.get("variants", [])
            for v in raw_variants:
                is_dirty = False
                text = v.get("text")
                raw_right_answer = v.get("right_answer")
                right_answer = False
                if raw_right_answer:
                    if raw_right_answer is True or raw_right_answer == "true":
                        right_answer = True
                    else:
                        right_answer = False

                raw_pair_object = v.get("pair_object")
                if raw_pair_object:
                    pair_id = raw_pair_object.get("id")
                    pair_text = raw_pair_object.get("text")
                    if pair_id:
                        variant_pair = page.variants.get(pk=pair_id)
                        if variant_pair.text != pair_text:
                            variant_pair.text = pair_text
                            variant_pair.save()

                id = v.get("id")
                if id:
                    variant = page.variants.get(pk=id)
                    if variant.text != text:
                        variant.text = text
                        is_dirty = True
                    if variant.right_answer != right_answer:
                        variant.right_answer = right_answer
                        is_dirty = True
                    if is_dirty is True:
                        variant.save()

        serializer = PageSerializer(instance=page)
        return Response(serializer.data)

    def create(self, request):
        if request.method == "POST":
            if request.body:
                req = json.loads(request.body.decode("utf-8"))

                if type(req) is dict:
                    text = req.get("text")
                    type_page = req.get("type")
                    number = req.get("number")
                    page = Page.objects.create(text=text, type=type_page, number=number)
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
                            page, created = Page.objects.get_or_create(pk=id)
                            if page.number != q.get('number'):
                                page.number = int(q.get('number'))
                                is_dirty = True
                            if is_dirty is True:
                                page.save()
                    return Response("OK", status=status.HTTP_200_OK)
            else:
                print "!!! create page"
        return Response("Error", status=status.HTTP_400_BAD_REQUEST)

    @detail_route(methods=['post'])
    def new_variant(self, request, *args, **kwargs):
        page_id = kwargs.get('id')
        if not page_id:
            res = {"code": 400, "message": "Bad Requset"}
            return Response(json.dumps(res), status=status.HTTP_200_OK)

        page = Page.objects.get(pk=page_id)
        text = request.data.get("text")

        raw_right_answer = request.data.get("right_answer", False)
        if raw_right_answer == "true":
            right_answer = True
        else:
            right_answer = False

        pair_type = request.data.get("pair_type")

        variant = page.variants.create(text=text, right_answer=right_answer)
        if pair_type:
            variant.pair_type = pair_type
            variant.save()

        raw_pair = request.data.get("pair")
        if raw_pair:
            pair = page.variants.get(id=raw_pair)
            if not pair:
                res = {"code": 400, "message": "Incorrect variant id"}
                return Response(json.dumps(res), status=status.HTTP_400_BAD_REQUEST)
            variant.pair = pair
            variant.save()

        serializer = VariantSerializer(instance=variant)
        return Response(serializer.data)

    @detail_route(methods=['delete'], url_path='remove_variant/(?P<variant_id>\d+)')
    def remove_variant(self, request, *args, **kwargs):
        page_id = kwargs.get('id')
        variant_id = kwargs.get('variant_id')

        if not page_id:
            res = {"code": 400, "message": "Incorrect page id"}
            return Response(json.dumps(res), status=status.HTTP_400_BAD_REQUEST)

        if not variant_id:
            res = {"code": 400, "message": "Incorrect variant id"}
            return Response(json.dumps(res), status=status.HTTP_400_BAD_REQUEST)

        variant = Variant.objects.get(pk=variant_id)

        if str(variant.page.id) != str(page_id):
            res = {"code": 400, "message": "Incorrect page id"}
            return Response(json.dumps(res), status=status.HTTP_400_BAD_REQUEST)

        variant.delete()
        return Response("OK")

# pageViewSet.as_view({'get': 'list'})


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
    data = EnrollSerializer(enroll).data
    data.update(LessonSerializer(lesson).data)
    return Response(data)


# назначеные на меня уроки
@api_view(['GET'])
def mylessons(request):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    enrolls = []
    for enroll in LessonEnroll.objects.filter(learner=request.user, is_archive=False):
        enrolls.append(EnrollSerializer(enroll).data)
    return Response(enrolls, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
def answers(request, enroll_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if request.method == 'PUT' and request.user.is_authenticated() and enroll_pk and enroll_pk != '0':
        enroll = get_object_or_404(LessonEnroll, pk=enroll_pk)
        if enroll.learner == request.user:
            data = json.loads(request.body.decode("utf-8"))
            result = data.get('result')
            if result:
                if not enroll.success:
                    enroll.success = result.get('success')
                enroll.number_of_attempt += 1
                enroll.last_data = timezone.now()

            enroll.data = data
            enroll.save()
            return Response(EnrollSerializer(enroll).data, status=status.HTTP_200_OK)

    if enroll_pk == '0':
        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT'])
@permission_classes((AllowAny, ))
def play(request, enroll_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    try:
        enroll = LessonEnroll.objects.get(pk=enroll_pk, learner=request.user)
    except LessonEnroll.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(EnrollSerializer(instance=enroll).data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT'])
@permission_classes((AllowAny, ))
def demo_play(request, lesson_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    try:
        lesson = Lesson.objects.get(pk=lesson_pk, created_by=request.user)
    except Lesson.DoesNotExist:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        if lesson.created_by == request.user:
            enroll = LessonEnroll(lesson=lesson, learner=request.user, created_by=request.user)

    return Response(EnrollSerializer(instance=enroll).data, status=status.HTTP_200_OK)

"""
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((AllowAny, ))
def lessons(request, lesson_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if request.method == 'GET' and request.user.is_authenticated():
        lessons = []
        if not lesson_pk:
            lessons = Lesson.objects.filter(created_by=request.user)
            if len(lessons) > 0:
                jsonlessons = []
                for l in lessons:
                    jsonlessons.append(LessonSerializer(l).data)
                return Response(jsonlessons, status=status.HTTP_200_OK)
            else:
                return Response([], status=status.HTTP_200_OK)
        else:
            try:
                lesson = Lesson.objects.get(pk=lesson_pk, created_by=request.user)
            except Lesson.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(LessonSerializer(instance=lesson).data, status=status.HTTP_200_OK)

    is_dirty = False
    is_active = None
    name = None
    description = None
    code_errors = None
    is_correct = None

    # create lesson
    if request.method == 'POST' and request.user.is_authenticated() and not lesson_pk:
        raw_data = request.body.decode("utf-8")

        if raw_data:
            req = json.loads(raw_data)
            is_active = req.get("is_active")
            name = req.get("name")
            description = req.get("description")
            code_errors = req.get("code_errors")
            is_correct = req.get("is_correct")

        lesson = Lesson.objects.create(created_by=request.user)
        if lesson.is_active != is_active and is_active is not None:
            lesson.is_active = is_active
            is_dirty = True
        if lesson.name != name and name is not None:
            lesson.name = name
            is_dirty = True
        if lesson.description != description and description is not None:
            lesson.description = description
            is_dirty = True
        if lesson.code_errors != code_errors and code_errors is not None:
            lesson.code_errors = code_errors
            is_dirty = True
        if lesson.is_correct != is_correct and is_correct is not None:
            lesson.is_correct = is_correct
            is_dirty = True

        if is_dirty is True:
            lesson.save()
        return Response(LessonSerializer(instance=lesson).data, status=status.HTTP_200_OK)

    if request.method == 'DELETE' and request.user.is_authenticated() and lesson_pk:
        lessons = Lesson.objects.filter(pk=lesson_pk, created_by=request.user)[:1]
        if len(lessons) > 0:
            lessons[0].delete()

    if request.method == 'PUT' and request.user.is_authenticated() and lesson_pk:
        req = json.loads(request.body.decode("utf-8"))
        is_dirty = False
        is_active = req.get("is_active")
        name = req.get("name")
        description = req.get("description")
        code_errors = req.get("code_errors")
        is_correct = req.get("is_correct")

        lesson = get_object_or_404(Lesson, pk=lesson_pk, created_by=request.user)
        if lesson.is_active != is_active:
            lesson.is_active = is_active
            is_dirty = True
        if lesson.name != name:
            lesson.name = name
            is_dirty = True
        if lesson.description != description:
            lesson.description = description
            is_dirty = True
        if lesson.code_errors != code_errors and code_errors is not None:
            lesson.code_errors = code_errors
            is_dirty = True
        if lesson.is_correct != is_correct and is_correct is not None:
            lesson.is_correct = is_correct
            is_dirty = True

        if is_dirty is True:
            lesson.save()
        return Response(LessonSerializer(instance=lesson).data, status=status.HTTP_200_OK)

    return Response([], status=status.HTTP_200_OK)
"""

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
        print "11 ", f
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
            archives.append(EnrollSerializer(instance=a).data)
        return Response(archives, status=status.HTTP_200_OK)

    if request.method == 'POST' and lesson_pk is not None:
        lessonEnrolls = LessonEnroll.objects.filter(lesson=lesson_pk, learner=request.user,
            is_archive=False)

        if len(lessonEnrolls) > 0:
            lessonEnroll = lessonEnrolls[0]
            lessonEnroll.is_archive = True
            lessonEnroll.date_archive = timezone.now()
            lessonEnroll.save()
            return Response(EnrollSerializer(instance=lessonEnroll).data, status=status.HTTP_200_OK)
        else:
            return Response([], status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
def get_mypupil(request):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)
    rawpupils = Account.objects.get(pk=request.user.pk).pupils.exclude(pk=request.user.pk)
    pupils_email = []
    for p in rawpupils:
        pupils_email.append(p.email)
    return Response(pupils_email, status=status.HTTP_200_OK)

"""
def validateEmail(email):
    if len(email) > 7:
        if re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) is not None:
            return True
    return False
"""

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
    try:
        LessonEnroll.objects.get(lesson=lesson, learner=pupil)
    except LessonEnroll.DoesNotExist:
        LessonEnroll.objects.create(lesson=lesson, learner=pupil, created_by=request.user)

    request.user.pupils.add(pupil)
    return Response("", status=status.HTTP_200_OK)


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((AllowAny,))
def enroll_pupil(request, enroll_pk):
    if not request.user.is_authenticated():
        return Response(status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        lesson_id = data.get('lesson_id')
        email = data.get('email')
        if validateEmail(email) is False:
            return Response("Неверный формат email", status=status.HTTP_400_BAD_REQUEST)
        lesson = get_object_or_404(Lesson, pk=lesson_id, created_by=request.user)
        pupil = Account.objects.filter(email__iexact=email)[:1]
        if pupil:
            try:
                enroll = LessonEnroll.objects.get(lesson=lesson, learner=pupil[0])
            except LessonEnroll.DoesNotExist:
                enroll = LessonEnroll.objects.create(lesson=lesson, learner=pupil[0], created_by=request.user)

            return Response(EnrollSerializer(enroll).data, status=status.HTTP_200_OK)
        else:
            return Response({'code': 404}, status=status.HTTP_200_OK)

    if request.method == 'DELETE' and enroll_pk:
        try:
            enroll = LessonEnroll.objects.get(pk=enroll_pk, lesson__created_by=request.user)
            enroll.delete()
        except LessonEnroll.DoesNotExist:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        return Response("", status=status.HTTP_200_OK)

    return Response(status=status.HTTP_200_OK)

