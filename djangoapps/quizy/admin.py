# -*- coding: utf-8 -*-

from django.contrib import admin
# from django.db.models import Q
from django.contrib.auth.models import Group


from quizy.models import Course, Lesson, CourseEnroll, LessonEnroll, Page, Variant
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
    list_display = ['learner', 'created_by', 'lesson', 'success', 'is_archive']
    # list_editable = ['is_active']
    list_filter = ['lesson__name']
    search_fields = ('learner__username', 'learner__first_name', 'learner__last_name', 'learner__email')
    readonly_fields = ['created_at', 'updated_at']


class LessonAdmin(admin.ModelAdmin):
    search_fields = ['course', 'name', 'created_by']
    list_filter = ['course']
    # fieldsets = (
    #    (None, {
    #        'fields': ('course', 'name', 'description', 'number', 'is_active', 'picture', 'is_correct', 'created_by')
    #    }),
    # )

    list_display = ['course', 'name', 'number', 'is_active', 'is_correct', 'is_correct']
    # list_editable = ['is_active']

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


admin.site.unregister(Group)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseEnroll, CourseEnrollAdmin)
admin.site.register(LessonEnroll, LessonEnrollAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Variant, VariantAdmin)
