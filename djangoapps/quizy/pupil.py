# -*- coding: utf-8 -*-

import json
from datetime import timedelta
# from HTMLParser import HTMLParser

# from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
# from django.db.models import Q

from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from quizy.models import (LessonEnroll, Statistic)
from quizy.serializers.serializers import (LessonEnrollSerializer)
from quizy.serializers.pupil import MyStatisticSerializer
from quizy.pagination import ListPagination
# from quizy.utils import normalize
from quizy.utils import is_enrolls_different


# назначеные на меня уроки
@api_view(['GET'])
def mylessons(request):
    """
    возвращает список назначеных на студента уроков
    """
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

    # Сериализуем и сортируем полученные уроки
    enrolls = []
    lessonEnrolls = LessonEnroll.objects.filter(learner=request.user).extra(
        select={'null_success': 'CASE WHEN quizy_lessonenroll.success IS NULL THEN 0 ELSE 1 END'}
    ).order_by('null_success', 'success', '-created_at')
    for enroll in lessonEnrolls:
        enrolls.append(LessonEnrollSerializer(enroll).data)

    index = 0
    elements = []
    for en in list(enrolls):
        if en.get('required_attention_by_pupil') is True:
            elements.append(enrolls.pop(index))
        index += 1
    sortedenrolls = elements + enrolls

    return Response(sortedenrolls, status=status.HTTP_200_OK)


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
    """
    перенос урока в архив
    """
    enroll = get_object_or_404(LessonEnroll, pk=enroll_pk)
    if enroll.learner == request.user:
        statistic = Statistic.objects.create(lesson=enroll.lesson,
            learner=enroll.learner, number_of_attempt=enroll.number_of_attempt,
            success=enroll.success, data=enroll.data)
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

        enroll.required_attention_by_pupil = False
        # if data.get('active') is False:
        #    enroll.required_attention_by_teacher = False
        # else:
        #    enroll.required_attention_by_teacher = True

        is_equal = is_enrolls_different(enroll.data, data)
        if is_equal is True:
            enroll.required_attention_by_teacher = True
            enroll.data = data
            enroll.data['mode'] = 'wait_teacher'
        else:
            enroll.data = data

        enroll.success = True
        enroll.save()

        # Делаем пометку в статистики
        raw_statistic = Statistic.objects.filter(lesson=enroll.lesson, learner=request.user)
        if not raw_statistic:
            statistic = Statistic.objects.create(lesson=enroll.lesson, learner=request.user)
        else:
            statistic = raw_statistic.latest('created_at')

        statistic.success = enroll.success = True
        statistic.save()

    enroll = LessonEnrollSerializer(instance=enroll).data
    return Response(enroll, status=status.HTTP_200_OK)
