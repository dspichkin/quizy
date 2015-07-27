# -*- coding: utf-8 -*-

import json

from rest_framework import serializers
from rest_framework import pagination
# from utils.serializers import JSONField

from users.account.serializers import UserSerializer
from users.account.models import Account
from quizy.models import Course, Lesson, CourseEnroll, LessonEnroll, Page, Variant


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
    pages = PageSerializer(many=True, read_only=True)
    code_errors = JSONField()
    material_type = serializers.CharField(source='type')

    class Meta:
        model = Lesson


class LessonEnrollSerializer(serializers.ModelSerializer):
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
    material_type = serializers.CharField(source='type')

    class Meta:
        model = Lesson


class CourseSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    lessons = LessonForCourseSerializer(source='lesson_set', many=True, read_only=True)
    code_errors = JSONField()
    material_type = serializers.CharField(source='type')
    enroll_number = serializers.ReadOnlyField()

    class Meta:
        model = Course
        exclude = ('teacher',)


class LessonSerializer(serializers.ModelSerializer):
    course = CourseSerializer(read_only=True)
    pages = PageSerializer(many=True, read_only=True)
    enrolls = LessonEnrollSerializer(many=True, read_only=True)
    code_errors = JSONField()
    material_type = serializers.CharField(source='type')

    class Meta:
        model = Lesson
