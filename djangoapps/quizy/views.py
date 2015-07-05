# -*- coding: utf-8 -*-

import json

# from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.core.mail import EmailMessage
from django.utils import timezone

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import detail_route
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from quizy.models import Lesson, Page, Variant, LessonEnroll
from quizy.serializers import EnrollSerializer, LessonSerializer, PageSerializer, VariantSerializer

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


@api_view(['GET', 'POST', 'DELETE'])
@permission_classes((AllowAny,))
def enroll_user(request, enroll_pk=None):
    """
    Назначить пользователя на курс
    """
    if request.method == 'POST':
        lesson_id = request.data.get('lesson_id')
        user_email = request.data.get('email')
        force = request.data.get('force', False)

        if not lesson_id or not user_email:
            res = {"code": 400, "message": "Incorrect request"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        if validateEmail(user_email) is False:
            res = {"code": 300, "message": "Incorrect email"}
            return Response(res, status=status.HTTP_200_OK)
        # Проверяем lesson_id
        lessons = Lesson.objects.filter(pk=lesson_id, created_by=request.user)
        lesson = None
        if not lessons:
            res = {"code": 400, "message": "Incorrect lesson_id"}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        else:
            lesson = lessons[0]
        # Проверяем наличие пользователя
        user_obj = None
        try:
            user_obj = Account.objects.get(email=user_email)
        except Account.DoesNotExist:
            if force is False:
                res = {"code": 200, "message": u"Пользователь с указанным Email не найден", "signal": "invite"}
                return Response(res, status=status.HTTP_200_OK)

        # проверяем было ли ранее такое назначение
        lessonEnrolls = LessonEnroll.objects.filter(
            learner=user_obj,
            lesson=lesson)
        if not lessonEnrolls:
            LessonEnroll.objects.create(
                learner=user_obj,
                lesson=lesson,
                is_active=True)

        bodies = {
            'html': 'Вам назначен урок %s' % (lesson)
        }
        msg = EmailMessage("Сообщение от Quizy",
                        bodies['html'],
                        settings.DEFAULT_FROM_EMAIL,
                        [user_obj.email])

        msg.content_subtype = 'html'
        msg.send()

        return Response({"code": 200, "message": u"Пользователь успешно назначен на урок", "signal": "success"}, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        try:
            enroll = LessonEnroll.objects.get(pk=enroll_pk, lesson__created_by=request.user)
            enroll.delete()
        except LessonEnroll.DoesNotExist:
            return Response("", status=status.HTTP_400_BAD_REQUEST)
        return Response("", status=status.HTTP_200_OK)


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
class MyLessonsViewSet(viewsets.ModelViewSet):
    serializer_class = LessonSerializer
    model = Lesson
    lookup_field = 'id'
    allowed_methods = ('GET', 'POST', 'PUT', 'DELETE')
    queryset = Lesson.objects.all()
    permission_classes = (AllowAny,)

    def get_queryset(self):
        if self.request.user.is_authenticated():
            lessons = []
            for l in LessonEnroll.objects.filter(learner=self.request.user, is_archive=False):
                lessons.append(l.lesson)
            return lessons
        return []


@api_view(['GET', 'POST'])
def answers(request, lesson_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if lesson_pk is not None:
        try:
            lesson = Lesson.objects.get(pk=lesson_pk)

            # если я создатель урока и нет назначение значит это тестирование
            if lesson.created_by == request.user:
                if lesson.enrolls.filter(learner=request.user).count() == 0:
                    return Response({"code": 200}, status=status.HTTP_200_OK)
            # иначе
            else:
                enrolls = lesson.enrolls.filter(learner=request.user)
                if len(enrolls) > 0:
                    enroll = enrolls[0]
                    answers = json.loads(request.body.decode("utf-8"))
                    enroll.result = answers
                    enroll.number_of_attempt += 1
                    _success = True
                    for a in answers:
                        if a.get('is_correct') is False:
                            _success = False
                    if enroll.success is not True:
                        enroll.success = _success
                    enroll.save()
                    return Response(EnrollSerializer(enroll).data, status=status.HTTP_200_OK)

        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)


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
            lessonEnrolls = LessonEnroll.objects.filter(lesson=lesson_pk, learner=request.user)
            if len(lessonEnrolls) > 0:
                for l in lessonEnrolls:
                    lessons.append(l.lesson)
            else:
                lessons = Lesson.objects.filter(created_by=request.user)

            if len(lessons) > 0:
                return Response(LessonSerializer(instance=lessons[0]).data, status=status.HTTP_200_OK)

    # create lesson
    if request.method == 'POST' and request.user.is_authenticated() and not lesson_pk:
        raw_data = request.body.decode("utf-8")

        is_dirty = False
        is_active = None
        name = None
        description = None

        if raw_data:
            req = json.loads(raw_data)
            is_active = req.get("is_active")
            name = req.get("name")
            description = req.get("description")

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
        if is_dirty is True:
            lesson.save()
        return Response(LessonSerializer(instance=lesson).data, status=status.HTTP_200_OK)

    return Response([], status=status.HTTP_200_OK)


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
