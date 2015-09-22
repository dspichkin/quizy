# -*- coding: utf-8 -*-

import json
from datetime import timedelta
from HTMLParser import HTMLParser

# from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from quizy.models import (LessonEnroll, Statistic)
from quizy.serializers.serializers import (LessonEnrollSerializer)
from quizy.serializers.pupil import MyStatisticSerializer
from quizy.pagination import ListPagination
from quizy.utils import normalize

# назначеные на меня уроки
@api_view(['GET'])
def mylessons(request):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    # проверяем есть ли старые пройденные уроки
    now = timezone.now()  # + timedelta(days=1)
    for enroll in LessonEnroll.objects.filter(learner=request.user, date_success__lt=now - timedelta(days=14)):
        statistic, created = Statistic.objects.get_or_create(lesson=enroll.lesson, learner=request.user,
            number_of_attempt=enroll.number_of_attempt, success=enroll.success)
        if enroll.success is True:
            statistic.reason = 'success'
        elif enroll.success is False:
            statistic.reason = 'done_time'
        else:
            statistic.reason = 'not_done'
        statistic.save()

        enroll.delete()
    for enroll in LessonEnroll.objects.filter(learner=request.user, success=True, date_success__lt=now - timedelta(days=1)):
        Statistic.objects.get_or_create(lesson=enroll.lesson, learner=request.user,
            number_of_attempt=enroll.number_of_attempt, success=enroll.success, reason='success')
        enroll.delete()
    enrolls = []
    for enroll in LessonEnroll.objects.filter(learner=request.user).order_by('-created_at'):
        enrolls.append(LessonEnrollSerializer(enroll).data)
    return Response(enrolls, status=status.HTTP_200_OK)


@csrf_exempt
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
                success = result.get('success')
                if not enroll.success:
                    enroll.success = success
                if success is True:
                    enroll.date_success = timezone.now()
                enroll.number_of_attempt += 1

            enroll.data = data
            enroll.save()
            return Response(LessonEnrollSerializer(enroll).data, status=status.HTTP_200_OK)

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
        return Response("enroll not found", status=status.HTTP_404_NOT_FOUND)

    return Response(LessonEnrollSerializer(instance=enroll).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def reject_lesson(request, enroll_pk):
    enroll = get_object_or_404(LessonEnroll, pk=enroll_pk)
    if enroll.learner == request.user:
        statistic = Statistic.objects.create(lesson=enroll.lesson,
            learner=enroll.learner, number_of_attempt=enroll.number_of_attempt,
            success=enroll.success)
        if enroll.success is None:
            statistic.reason = 'reject'
            statistic.save()

        enroll.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
def mystatistic(request):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    qs = Statistic.objects.filter(learner=request.user)

    paginator = ListPagination()
    result_page = paginator.paginate_queryset(qs, request)
    serializer = MyStatisticSerializer(result_page, many=True)

    return paginator.get_paginated_response(serializer.data)


@api_view(['PUT'])
def enroll_pupil(request, enroll_pk):
    """
    Сохраняет данные для назначения со стороны ученика
    """
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    if enroll_pk:
        try:
            enroll = LessonEnroll.objects.get(learner=request.user, pk=enroll_pk)
        except LessonEnroll.DoesNotExist:
            return Response(status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'PUT':
        data = json.loads(request.body.decode("utf-8"))
        # enroll.data = normalize(data)
        enroll.data = data

        enroll.required_attention_by_pupil = False
        if data.get('active') is False:
            enroll.required_attention_by_teacher = False
        else:
            enroll.required_attention_by_teacher = True
        enroll.success = True
        enroll.save()

        # Делаем пометку в статистики
        statistic, created = Statistic.objects.get_or_create(lesson=enroll.lesson, learner=request.user)
        statistic.success = enroll.success = True
        statistic.save()

    enroll = LessonEnrollSerializer(instance=enroll).data
    return Response(enroll, status=status.HTTP_200_OK)
