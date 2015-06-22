# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, division

# from .models import User, Organization, EmailAddress
from .models import User, Organization, EmailConfirmation
from rest_framework import serializers




class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'fio')


#class EmailSerializer(serializers.ModelSerializer):
#    class Meta:
#        model = EmailAddress
#        exclude = ('id', 'user')

"""
class InviteSerializer(serializers.ModelSerializer):
    course_id = serializers.ReadOnlyField(source='course.pk')
    user = SimpleUserSerializer()

    class Meta:
        model = Invite
        fields = ('id', 'course_id', 'user')
"""


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ReadOnlyField(source='get_avatar_url')
    fio = serializers.ReadOnlyField()
    # emails = EmailSerializer(source='emailaddress_set', many=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            # 'invites',
            'fio',
            'first_name',
            'middle_name',
            'last_name',
            'avatar',
            'role',
            'last_login',
            'date_joined'
        )


class EmailConfirmationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = EmailConfirmation


class AdminSerializer(serializers.ModelSerializer):
    avatar = serializers.ReadOnlyField(source='get_avatar_url')
    fio = serializers.ReadOnlyField()
    # invites = InviteSerializer(many=True)
    #emails = EmailSerializer(source='emailaddress_set', many=True)
    members = SimpleUserSerializer(source='org.accounts', many=True)

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            # 'invites',
            'fio',
            'first_name',
            'middle_name',
            'last_name',
            'avatar',
            'role',
            'members',
            'last_login',
            'date_joined'
        )


