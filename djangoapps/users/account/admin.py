# -*- coding: utf-8 -*-
#
import django
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import (Account,
    EmailConfirmation, SystemMessage)
from .adapter import get_adapter

"""
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'primary', 'verified')
    list_filter = ('primary', 'verified')
    search_fields = []
    raw_id_fields = ('user',)

    def __init__(self, *args, **kwargs):
        super(EmailAddressAdmin, self).__init__(*args, **kwargs)
        if not self.search_fields and django.VERSION[:2] < (1, 7):
            self.search_fields = self.get_search_fields(None)

    def get_search_fields(self, request):
        base_fields = get_adapter().get_user_search_fields()
        return ['email'] + list(map(lambda a: 'user__' + a, base_fields))
"""


class EmailConfirmationAdmin(admin.ModelAdmin):
    # list_display = ('email_address', 'created', 'sent', 'key')
    list_display = ('user', 'created', 'sent', 'key')
    list_filter = ('sent',)
    # raw_id_fields = ('user__email',)
from django import forms

class AccountAdmin(UserAdmin):
    list_display = ('username', 'account_type', 'number_of_pupil', 'is_active', 'verified', 'is_superuser')
    # fieldsets = UserAdmin.fieldsets
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (u'Персональная информация', {'fields': ('first_name', 'last_name', 'middle_name', 'email')}),
        (u'Права доступа', {'fields': ('is_active', 'is_staff', 'is_superuser',)}),  # 'groups', 'user_permissions'
        (
            u'Дополнения', {
                'classes': ('wide',),
                'fields': ('avatar', 'account_type', 'pupils')
            }
        )
    )
    # fieldsets = (extra_fieldsets)

    filter_horizontal = ('pupils', )

    def clean(self):
        super(AccountAdmin, self).clean()
        # Validation goes here :)
        print "username", self.cleaned_data["username"] 
        print "email", self.cleaned_data["email"] 

        raise forms.ValidationError("TEST EXCEPTION!")


class SystemMessageAdmin(admin.ModelAdmin):
    pass


admin.site.register(EmailConfirmation, EmailConfirmationAdmin)
# admin.site.register(EmailAddress, EmailAddressAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(SystemMessage, SystemMessageAdmin)
