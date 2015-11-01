# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import os

from django.conf import settings
from django import forms
from django.forms import ModelForm
from django.contrib.admin.widgets import FilteredSelectMultiple

from suit_redactor.widgets import RedactorWidget
from users.account.models import Account

from quizy.models import (Course, Lesson, CourseEnroll, LessonEnroll, Page, Variant,
    Statistic, Tag)

"""
class ContentChoiceField(forms.ChoiceField):
    def prepare_value(self, data):
        # print ('PREPARE', data, self.instance)
        #if data and self.instance.pk:
        #    return '%s.%s' % (self.instance.content_type.pk, data)
        return data



class LessonForm1(forms.ModelForm):
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
     equired=True
    # )

    class Meta:
        model = Lesson
        fields = ('name', 'is_active', 'description', 'created_by', )

"""


class LessonForm(ModelForm):
    class Meta:
        widgets = {
            'description': RedactorWidget(editor_options={'lang': 'ru'}),
        }

    teacher = forms.ModelMultipleChoiceField(label=u'Преподователь', queryset=Account.objects.filter(account_type=1), widget=FilteredSelectMultiple(u"Преподователи", is_stacked=False))
    tag = forms.ModelMultipleChoiceField(label=u'Метки', queryset=Tag.objects.all(), widget=FilteredSelectMultiple(u"Метки", is_stacked=False), required=False)


class CourseForm(ModelForm):
    class Meta:
        widgets = {
            'description': RedactorWidget(editor_options={'lang': 'ru'}),
        }

    teacher = forms.ModelMultipleChoiceField(label=u'Преподователь', queryset=Account.objects.filter(account_type=1), widget=FilteredSelectMultiple(u"Преподователи", is_stacked=False))


class LessonEnrollForm(ModelForm):

    teachers = forms.ModelMultipleChoiceField(label=u'Преподователь', queryset=Account.objects.filter(account_type=1), widget=FilteredSelectMultiple(u"Преподователи", is_stacked=False))

