# -*- coding: utf-8 -*-

from django.contrib import admin
from django.db.models import Q
from django.contrib.auth.models import Group


from quizy.models import Course, Lesson, LessonEnroll, Page, Variant
# from quizy.forms import LessonForm



class CourseAdmin(admin.ModelAdmin):
    pass


class EnrollAdmin(admin.ModelAdmin):
    list_display = ['learner', 'is_archive']
    # list_editable = ['is_active']
    list_filter = ['lesson__name']
    search_fields = ('learner__username', 'learner__first_name', 'learner__last_name', 'learner__email')
    actions = ['lock']
    readonly_fields = ['created_at', 'updated_at']

    def lock(self, request, queryset):
        # rows_updated = queryset.update(is_active=False)
        self.message_user(request, 'Успешно закрыто %d назначений')
    lock.short_description = 'Закрыть выбранные назначения'


class LessonAdmin(admin.ModelAdmin):
    search_fields = ['name', 'created_by']
    readonly_fields = ('created_by',)
    fieldsets = (
        (None, {
            'fields': ('name', 'description', 'is_active', 'created_by')
        }),
    )

    list_display = ['created_by', 'name', 'is_active', ]
    # list_editable = ['is_active']

    # actions = ['delete_selected']

    #def num_learners(self, obj):
    #    return obj.enrolls.filter(
    #        Q(is_active=True)).count()

    def save_model(self, request, obj, form, change):
        if getattr(obj, 'created_by', None) is None:
            obj.created_by = request.user
        obj.save()


class PageAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'type', 'number', ]


class VariantAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(Group)
admin.site.register(Course,CourseAdmin)
admin.site.register(LessonEnroll, EnrollAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Variant, VariantAdmin)
