# -*- coding: utf-8 -*-
import os.path

from django.contrib import admin
# from django.db.models import Q
from django.contrib.auth.models import Group
from django.forms import ModelForm
from django import forms

from suit_redactor.widgets import RedactorWidget
from sorl.thumbnail import get_thumbnail

from quizy.models import (Course, Lesson, CourseEnroll, LessonEnroll, Page, Variant,
    Statistic)
from users.account.models import Account
# from quizy.forms import LessonForm


class CourseAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_by', 'is_active', 'is_correct', 'get_teacher']

    class Media:
        css = {
            'all': (
                'css/admin/course.css',
            )
        }

    def get_teacher(self, obj):
        return ", ".join([x.email for x in obj.teacher.all()])

    get_teacher.short_description = u"Преподователи"


class CourseEnrollAdmin(admin.ModelAdmin):
    list_display = ['learner', 'created_by', 'success', 'is_archive']
    search_fields = ('learner__username', 'learner__first_name', 'learner__last_name', 'learner__email')
    readonly_fields = ['created_at', 'updated_at']


class LessonEnrollAdmin(admin.ModelAdmin):
    list_display = ['learner', 'created_by', 'lesson', 'success', 'date_success']
    # list_editable = ['is_active']
    list_filter = ['lesson__name']
    search_fields = ('learner__username', 'learner__first_name', 'learner__last_name', 'learner__email')
    readonly_fields = ['created_at', 'updated_at']

    class Media:
        css = {
            'all': (
                'css/run_ace.css',
            )
        }
        js = (
            'js/ace/ace.js',
            'js/run_ace.js',
        )

from django.contrib.admin.widgets import FilteredSelectMultiple


class LessonForm(ModelForm):
    class Meta:
        widgets = {
            'description': RedactorWidget(editor_options={'lang': 'ru'}),
        }

    teacher = forms.ModelMultipleChoiceField(label=u'Преподователь', queryset=Account.objects.filter(account_type=1), widget=FilteredSelectMultiple(u"Преподователи", is_stacked=False))


class LessonAdmin(admin.ModelAdmin):
    form = LessonForm
    list_display = ['course', 'name', 'number', 'full_lesson_type', 'is_active', 'is_correct', 'is_correct']
    search_fields = ('course', 'name', 'created_by')
    list_filter = ('lesson_type', 'course', )
    readonly_fields = ('picture_thumbnail', 'media_thumbnail')
    fieldsets = (
        (
            u'Основные', {
                'classes': ('wide', 'full-width',),
                'fields': ('course', 'name', 'description', 'is_active', 'number', 'picture_thumbnail', 'picture', 'is_correct', 'is_public')
            }
        ), (
            u'Дополнительные', {
                'classes': ('wide', 'full-width',),
                'fields': ('created_by', 'teacher', 'full_lesson_type', 'media_thumbnail', 'media', 'timer')
            }
        )
    )

    def picture_thumbnail(self, obj):
        if obj.picture:
            ext = os.path.splitext(str(obj.picture))[1]
            if ext in ['.jpg', '.png']:
                return u'<img src="/media/%s" />' % get_thumbnail(obj.picture, '100x100', crop='center')
            else:
                return obj.picture
        else:
            return 'None'
    picture_thumbnail.short_description = 'предпросмотр картинки урока'
    picture_thumbnail.allow_tags = True

    def media_thumbnail(self, obj):
        if obj.media:
            ext = os.path.splitext(str(obj.media))[1]
            if ext in ['.jpg', '.png']:
                return u'<img src="/media/%s" />' % get_thumbnail(obj.media, '100x100', crop='center')
            else:
                return obj.media
        else:
            return 'None'
    media_thumbnail.short_description = 'предпросмотр медиа урока'
    media_thumbnail.allow_tags = True

    # actions = ['delete_selected']
    class Media:
        css = {
            'all': (
                'css/admin/course.css',
            )
        }

    def get_teacher(self, obj):
        return ", ".join([x.email for x in obj.teacher.all()])

    get_teacher.short_description = u"Преподователи"

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


class PageAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'type', 'number', ]


class VariantAdmin(admin.ModelAdmin):
    pass


class StatisticAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'learner', 'created_at', 'success', 'reason']


admin.site.unregister(Group)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseEnroll, CourseEnrollAdmin)
admin.site.register(LessonEnroll, LessonEnrollAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Variant, VariantAdmin)
admin.site.register(Statistic, StatisticAdmin)

