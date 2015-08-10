# -*- coding: utf-8 -*-

import json

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from quizy.models import Course, Lesson
from quizy.serializers.serializers import (CourseSerializer, LessonSerializer)
from quizy.pagination import ListPagination


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((AllowAny, ))
def courses(request, course_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if request.method == 'GET' and request.user.is_authenticated():
        if not course_pk:
            # возвращаем список всех курсов и уроков
            qs = Course.objects.filter(Q(created_by=request.user) | Q(teacher=request.user))

            paginator = ListPagination()
            result_page = paginator.paginate_queryset(qs, request)
            serializer = CourseSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        else:
            try:
                course = Course.objects.get(Q(created_by=request.user) | Q(teacher=request.user), pk=course_pk)
                coursejson = CourseSerializer(course).data
            except Course.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(coursejson, status=status.HTTP_200_OK)


@csrf_exempt
@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((AllowAny, ))
def lessons(request, lesson_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if request.method == 'GET' and request.user.is_authenticated():
        lessons = []
        if not lesson_pk:
            # возвращаем список всех курсов и уроков
            qs = Lesson.objects.filter(Q(created_by=request.user) | Q(teacher=request.user))
            lessons = LessonSerializer(qs, many=True).data
            return Response(lessons, status=status.HTTP_200_OK)
        else:
            try:
                lesson = Lesson.objects.get(Q(created_by=request.user) | Q(teacher=request.user) | Q(course__teacher=request.user), pk=lesson_pk)
                lessonsjson = LessonSerializer(lesson).data
            except Lesson.DoesNotExist:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(lessonsjson, status=status.HTTP_200_OK)

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
            course_id = req.get("course")

        course = get_object_or_404(Course, pk=course_id)
        # выставляем текущий номер урока в курсе
        number_lesson = course.lesson_set.all().count() + 1
        lesson = Lesson.objects.create(course=course, number=number_lesson, created_by=request.user)

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
            lesson.set_code_errors(code_errors)
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
        return Response(status=status.HTTP_200_OK)

    if request.method == 'PUT' and request.user.is_authenticated() and lesson_pk:
        req = json.loads(request.body.decode("utf-8"))
        is_dirty = False
        is_active = req.get("is_active")
        name = req.get("name")
        description = req.get("description")
        code_errors = req.get("code_errors")
        is_correct = req.get("is_correct")
        try:
            lesson = Lesson.objects.get(Q(created_by=request.user) | Q(teacher=request.user) | Q(course__teacher=request.user), pk=lesson_pk)
        except Lesson.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
            lesson.set_code_errors(code_errors)
            is_dirty = True
        if lesson.is_correct != is_correct and is_correct is not None:
            lesson.is_correct = is_correct
            is_dirty = True

        if is_dirty is True:
            lesson.save()
        return Response(LessonSerializer(instance=lesson).data, status=status.HTTP_200_OK)

    return Response([], status=status.HTTP_200_OK)
