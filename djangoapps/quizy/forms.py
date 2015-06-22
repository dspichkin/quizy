# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django import forms

from .models import Lesson

"""
class ContentChoiceField(forms.ChoiceField):
    def prepare_value(self, data):
        # print ('PREPARE', data, self.instance)
        #if data and self.instance.pk:
        #    return '%s.%s' % (self.instance.content_type.pk, data)
        return data
"""


class LessonForm(forms.ModelForm):
    CONTENT_STATUS_CHOICES = (
        (True, 'активный'),
        (False, 'неактивный')
    )

    is_active = forms.ChoiceField(
        label="Статус урока",
        choices=CONTENT_STATUS_CHOICES,
        initial=True, required=True,
        help_text=("Активный курс отображается в списке курсов"
                   "у пользователя; неактивный курс — не "
                   "отображется, по сути такой курс закрыт.")
    )

    name = forms.CharField(
        label="Название курса",
        required=True,
        max_length=50,
        help_text=("Короткое название. \
                    Этот текст будет виден в списке курсов.")
    )

    description = forms.CharField(
        label="Описание курса",
        widget=forms.Textarea,
        required=False,
        help_text=("Более подробное описание курса. \
                    Этот текст будет виден в списке курсов.")
    )

    created_by = forms.CharField(
        label="Создатель курса",
        required=False,
        widget=forms.TextInput(attrs={'readonly': 'readonly'}),
        help_text=("")
    )

    # path = ContentChoiceField(
    #    label="Содержание",
    #    required=True
    # )

    class Meta:
        model = Lesson
        fields = ('name', 'is_active', 'description', 'created_by', )

    """
    def __init__(self, *args, **kwargs):
        super(LessonForm, self).__init__(*args, **kwargs)

        courses = [('', '---------')]

        base_path = os.path.join(settings.BASE_DIR, 'app', 'assets', 'courses')
        for d in os.listdir(base_path):
            content_path = os.path.join(base_path, d)
            if d[0] not in '_.' and os.path.isdir(content_path):
                courses.append((d, d))

        self.fields['path'].choices = courses
        self.fields['path'].widget = forms.Select(choices=courses, attrs={'class': 'form-control'})
    """
