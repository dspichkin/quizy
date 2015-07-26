# -*- coding: utf-8 -*-

import json

from rest_framework import serializers
# from utils.serializers import JSONField

from users.account.serializers import UserSerializer
from users.account.models import Account
from quizy.models import Course, Lesson, CourseEnroll, LessonEnroll


class CourseForPupilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        exclude = ('teacher',)


class LessonForPupilSerializer(serializers.ModelSerializer):
    course = CourseForPupilSerializer(read_only=True)

    class Meta:
        model = Lesson


class LessonEnrollForPupilSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    lesson = LessonForPupilSerializer(read_only=True)

    class Meta:
        model = LessonEnroll
        exclude = ("data",)


class CourseEnrollForPupilSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    course = CourseForPupilSerializer(read_only=True)

    class Meta:
        model = CourseEnroll
        exclude = ("data",)


class PupilSerializer(serializers.ModelSerializer):
    lesson_enrolls = LessonEnrollForPupilSerializer(many=True, read_only=True)
    course_enrolls = CourseEnrollForPupilSerializer(many=True, read_only=True)

    class Meta:
        model = Account
