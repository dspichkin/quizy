# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import users.socialaccount.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='SocialAccount',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(max_length=30, verbose_name='provider')),
                ('uid', models.CharField(max_length=255, verbose_name='uid')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='last login')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='date joined')),
                ('extra_data', users.socialaccount.fields.JSONField(default=b'{}', verbose_name='extra data')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'social account',
                'verbose_name_plural': 'social accounts',
            },
        ),
        migrations.CreateModel(
            name='SocialApp',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('provider', models.CharField(max_length=30, verbose_name='provider')),
                ('name', models.CharField(max_length=40, verbose_name='name')),
                ('client_id', models.CharField(help_text='App ID, or consumer key', max_length=100, verbose_name='client id')),
                ('secret', models.CharField(help_text='API secret, client secret, or consumer secret', max_length=100, verbose_name='secret key')),
                ('key', models.CharField(help_text='Key', max_length=100, verbose_name='key', blank=True)),
            ],
            options={
                'verbose_name': 'social application',
                'verbose_name_plural': 'social applications',
            },
        ),
        migrations.CreateModel(
            name='SocialToken',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.TextField(help_text='"oauth_token" (OAuth1) or access token (OAuth2)', verbose_name='token')),
                ('token_secret', models.TextField(help_text='"oauth_token_secret" (OAuth1) or refresh token (OAuth2)', verbose_name='token secret', blank=True)),
                ('expires_at', models.DateTimeField(null=True, verbose_name='expires at', blank=True)),
                ('account', models.ForeignKey(to='socialaccount.SocialAccount')),
                ('app', models.ForeignKey(to='socialaccount.SocialApp')),
            ],
            options={
                'verbose_name': 'social application token',
                'verbose_name_plural': 'social application tokens',
            },
        ),
        migrations.AlterUniqueTogether(
            name='socialtoken',
            unique_together=set([('app', 'account')]),
        ),
        migrations.AlterUniqueTogether(
            name='socialaccount',
            unique_together=set([('provider', 'uid')]),
        ),
    ]
