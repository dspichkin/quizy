# -*- coding: utf-8 -*-

import json

from rest_framework import serializers
from sorl_thumbnail_serializer.fields import HyperlinkedSorlImageField

from users.account.serializers import UserSerializer
from quizy.models import (Course, Lesson, CourseEnroll, LessonEnroll,
    Page, Variant, Statistic)


class JSONField(serializers.Field):
    """
    Сериализация JSON-полей
    """
    def __init__(self, default=None, **kwargs):
        super(JSONField, self).__init__(**kwargs)
        self.default = default

    def to_representation(self, obj):
        if isinstance(obj, basestring):
            try:
                return json.loads(obj)
            except ValueError:
                return json.loads(self.default)
        return obj

    def to_internal_value(self, data):
        return json.dumps(data, ensure_ascii=False)


class VariantSerializer(serializers.ModelSerializer):
    code_errors = JSONField()

    class Meta:
        model = Variant


class PageSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)
    code_errors = JSONField()

    class Meta:
        model = Page


# class LessonEnrollSerializer(serializers.ModelSerializer):
#    pages = PageSerializer(many=True, read_only=True)

#    class Meta:
#        model = Lesson


class CourseEnrollSerializer(serializers.ModelSerializer):
    learner = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    data = JSONField()

    class Meta:
        model = CourseEnroll
        exclude = ("data",)


class LessonForEnrollSerializer(serializers.ModelSerializer):
    # pages = PageSerializer(many=True, read_only=True)
    code_errors = JSONField()
    content = JSONField()
    thumbnail_picture = HyperlinkedSorlImageField(
        '158x100',
        options={"crop": "center"},
        source='picture',
        read_only=True
    )

    class Meta:
        model = Lesson
        # exclude = ("pages",)


class LessonEnrollSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField()
    updated_at = serializers.DateTimeField()
    learner = UserSerializer(read_only=True)
    created_by = UserSerializer(read_only=True)
    data = JSONField()
    lesson = LessonForEnrollSerializer(read_only=True)

    class Meta:
        model = LessonEnroll
        exclude = ("data",)


class EnrollForCourseSerializer (serializers.ModelSerializer):
    learner = UserSerializer(read_only=True)

    class Meta:
        model = LessonEnroll
        exclude = ("data",)


class LessonForCourseSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)
    enrolls = EnrollForCourseSerializer(many=True, read_only=True)
    code_errors = JSONField()

    class Meta:
        model = Lesson


class CourseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    lessons = LessonForCourseSerializer(source='lesson_set', many=True, read_only=True)
    code_errors = JSONField()
    enroll_number = serializers.ReadOnlyField()

    class Meta:
        model = Course
        exclude = ('teacher',)


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    pages = PageSerializer(many=True, read_only=True)
    enrolls = LessonEnrollSerializer(many=True, read_only=True)
    code_errors = JSONField()

    class Meta:
        model = Lesson


class CourseForStatisticSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Course
        exclude = ('teacher',)


class LessonForStatisticSerializer(serializers.ModelSerializer):
    course = CourseForStatisticSerializer(read_only=True)

    class Meta:
        model = Lesson


class StatisticSerializer(serializers.ModelSerializer):
    lesson = LessonForStatisticSerializer(read_only=True)
    learner = UserSerializer(read_only=True)

    class Meta:
        model = Statistic
