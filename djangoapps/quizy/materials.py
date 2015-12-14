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
from users.account.serializers import UserSerializer


@api_view(['GET', 'POST', 'PUT', 'DELETE'])
@permission_classes((AllowAny, ))
def courses(request, course_pk=None):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if request.method == 'GET' and request.user.is_authenticated():
        if not course_pk:
            # возвращаем список всех курсов и уроков
            qs = Course.objects.filter(Q(created_by=request.user) | Q(teacher=request.user)).distinct()
            paginator = ListPagination()
            result_page = paginator.paginate_queryset(qs, request)
            serializer = CourseSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        else:
            course = Course.objects.filter(Q(created_by=request.user) | Q(teacher=request.user), pk=course_pk).distinct()
            if course:
                course = course[0]
                lessons = []
                for lesson in course.lesson_set.all():
                    temp_lesson = {}
                    temp_enrolls = []
                    for enroll in lesson.enrolls.all():
                        exist = request.user.pupils.filter(pk=enroll.learner.pk).count()
                        if exist:
                            temp_enroll = {}
                            temp_enroll["learner"] = {
                                "email": enroll.learner.email
                            }
                            temp_enroll["id"] = enroll.id
                            temp_enroll["lesson"] = enroll.lesson.pk
                            temp_enroll["required_attention_by_pupil"] = enroll.required_attention_by_pupil
                            temp_enroll["required_attention_by_teacher"] = enroll.required_attention_by_teacher
                            temp_enroll["number_of_attempt"] = enroll.number_of_attempt
                            temp_enroll["updated_at"] = enroll.updated_at

                            temp_enrolls.append(temp_enroll)

                    temp_lesson["enrolls"] = temp_enrolls
                    temp_lesson["id"] = lesson.pk
                    temp_lesson["name"] = lesson.name
                    temp_lesson["number"] = lesson.number
                    temp_lesson["description"] = lesson.description
                    #temp_lesson["picture"] = lesson.picture
                    temp_lesson["full_lesson_type"] = lesson.full_lesson_type
                    temp_lesson["lesson_type"] = lesson.lesson_type
                    temp_lesson["path_content"] = lesson.path_content
                    #temp_lesson["media"] = lesson.media.
                    temp_lesson["timer"] = lesson.timer
                    temp_lesson["created_by"] = lesson.created_by.pk
                    temp_lesson["course"] = lesson.course.pk
                    lessons.append(temp_lesson)

                data = {
                    "lessons": lessons,
                    "name": course.name,
                    "description": course.description,
                    "is_correct": course.is_correct,
                }
                # coursejson = CourseSerializer(course).data
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(data, status=status.HTTP_200_OK)


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
            qs = Lesson.objects.filter(Q(created_by=request.user) | Q(teacher=request.user)).distinct()
            lessons = LessonSerializer(qs, many=True).data
            return Response(lessons, status=status.HTTP_200_OK)
        else:
            lesson = Lesson.objects.filter(Q(created_by=request.user) | Q(teacher=request.user) | Q(course__teacher=request.user), pk=lesson_pk).distinct()
            if lesson:
                lessonsjson = LessonSerializer(lesson[0]).data
                return Response(lessonsjson, status=status.HTTP_200_OK)
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST)

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
        lesson = Lesson.objects.create(course=course, number=number_lesson, created_by=request.user, lesson_type='inside', full_lesson_type=1)

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
        lesson = Lesson.objects.filter(Q(created_by=request.user) | Q(teacher=request.user) | Q(course__teacher=request.user), pk=lesson_pk).distinct()
        if lesson:
            lesson = lesson[0]
        else:
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
