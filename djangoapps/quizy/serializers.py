# -*- coding: utf-8 -*-

import json

from rest_framework import serializers
# from utils.serializers import JSONField

from users.account.serializers import UserSerializer
from quizy.models import Lesson, LessonEnroll, Page, Variant


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

    class Meta:
        model = Variant


class PageSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True)
    code_errors = JSONField()

    class Meta:
        model = Page


class LessonEnrollSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson


class EnrollSerializer(serializers.ModelSerializer):
    learner = UserSerializer(read_only=True)
    result = JSONField()
    lesson = LessonEnrollSerializer(read_only=True)

    class Meta:
        model = LessonEnroll


class LessonSerializer(serializers.ModelSerializer):
    pages = PageSerializer(many=True, read_only=True)
    enrolls = EnrollSerializer(many=True, read_only=True)
    code_errors = JSONField()

    class Meta:
        model = Lesson






