# -*- coding: utf-8 -*-

import json

# from django.views.generic import TemplateView
from django.shortcuts import get_object_or_404
from django.utils import timezone


from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes

from quizy.models import (LessonEnroll, Statistic)
from quizy.serializers.serializers import (LessonEnrollSerializer)


# назначеные на меня уроки
@api_view(['GET'])
def mylessons(request):
    if not request.user.is_authenticated():
        return Response([], status=status.HTTP_200_OK)

    enrolls = []
    for enroll in LessonEnroll.objects.filter(learner=request.user, is_archive=False).order_by('-created_at'):
        enrolls.append(LessonEnrollSerializer(enroll).data)
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
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(LessonEnrollSerializer(instance=enroll).data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def reject_lesson(request, enroll_pk):
    enroll = get_object_or_404(LessonEnroll, pk=enroll_pk)
    print "!!!!", enroll.learner
    if enroll.learner == request.user:
        print "!!!!"
        Statistic.objects.create(lesson=enroll.lesson,
            learner=enroll.learner, number_of_attempt=enroll.number_of_attempt,
            success=enroll.success)
        enroll.delete()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
