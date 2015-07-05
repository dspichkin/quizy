# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Attempt',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_best', models.BooleanField(default=False, editable=False)),
                ('is_last', models.BooleanField(default=False, editable=False)),
                ('points', models.IntegerField(default=0)),
                ('num', models.PositiveIntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('duration', models.IntegerField(default=0)),
                ('data', json_field.fields.JSONField(default=b'{}', help_text='Enter a valid JSON object')),
            ],
            options={
                'verbose_name': '\u041f\u043e\u043f\u044b\u0442\u043a\u0430',
                'verbose_name_plural': '\u041f\u043e\u043f\u044b\u0442\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=36, editable=False, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name=b'\xd0\xb0\xd0\xba\xd1\x82\xd0\xb8\xd0\xb2\xd0\xb5\xd0\xbd?')),
                ('name', models.CharField(max_length=140, null=True, verbose_name=b'\xd0\xbd\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xba\xd1\x83\xd1\x80\xd1\x81\xd0\xb0', blank=True)),
                ('description', models.TextField(verbose_name=b'\xd0\xbe\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', blank=True)),
            ],
            options={
                'verbose_name': '\u041a\u0443\u0440\u0441',
                'verbose_name_plural': '\u041a\u0443\u0440\u0441\u044b',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=36, editable=False, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name=b'\xd0\xb0\xd0\xba\xd1\x82\xd0\xb8\xd0\xb2\xd0\xb5\xd0\xbd?')),
                ('name', models.CharField(max_length=140, null=True, verbose_name=b'\xd0\xbd\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0', blank=True)),
                ('number', models.IntegerField(default=0, verbose_name=b'\xd0\xbf\xd0\xbe\xd1\x80\xd1\x8f\xd0\xb4\xd0\xbe\xd0\xba \xd1\x81\xd0\xbb\xd0\xb5\xd0\xb4\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('description', models.TextField(verbose_name=b'\xd0\xbe\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5', blank=True)),
                ('course', models.ForeignKey(verbose_name=b'\xd0\xba\xd1\x83\xd1\x80\xd1\x81', blank=True, to='quizy.Course', null=True)),
                ('created_by', models.ForeignKey(related_name='lessons', verbose_name=b'\xd1\x81\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'ordering': ('created_by', 'number'),
                'verbose_name': '\u0423\u0440\u043e\u043a',
                'verbose_name_plural': '\u0423\u0440\u043e\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='LessonEnroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.CharField(unique=True, max_length=36, editable=False, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('result', json_field.fields.JSONField(default=b'{}', help_text='Enter a valid JSON object', verbose_name=b'\xd1\x80\xd0\xb5\xd0\xb7\xd1\x83\xd0\xbb\xd1\x8c\xd1\x82\xd0\xb0\xd1\x82 \xd0\xbf\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb6\xd0\xb4\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('number_of_attempt', models.IntegerField(default=0, verbose_name=b'\xd0\xba\xd0\xbe\xd0\xbb-\xd0\xb2\xd0\xbe \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xbe\xd0\xba')),
                ('success', models.NullBooleanField(verbose_name=b'\xd1\x80\xd0\xb5\xd0\xb7\xd1\x83\xd0\xbb\xd1\x8c\xd1\x82\xd0\xb0\xd1\x82 \xd0\xbf\xd0\xbe\xd1\x81\xd0\xbb\xd0\xb5\xd0\xb4\xd0\xbd\xd0\xb5\xd0\xb9 \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xba\xd0\xb8 \xd0\xbf\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb6\xd0\xb4\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('is_archive', models.BooleanField(default=False, verbose_name=b'\xd1\x83\xd1\x80\xd0\xbe\xd0\xba \xd0\xb2 \xd0\xb0\xd1\x80\xd1\x85\xd0\xb8\xd0\xb2\xd0\xb5')),
                ('date_archive', models.DateTimeField(null=True, verbose_name=b'\xd0\xb4\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xb5\xd1\x80\xd0\xb5\xd0\xbc\xd0\xb5\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xb2 \xd0\xb0\xd1\x80\xd1\x85\xd0\xb8\xd0\xb2\xd0\xb5', blank=True)),
                ('course', models.ForeignKey(related_name='enrolls', verbose_name=b'\xd0\xba\xd1\x83\xd1\x80\xd1\x81', blank=True, to='quizy.Course', null=True)),
                ('learner', models.ForeignKey(related_name='enrolls', verbose_name=b'\xd0\xbe\xd0\xb1\xd1\x83\xd1\x87\xd0\xb0\xd0\xb5\xd0\xbc\xd1\x8b\xd0\xb9', to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(related_name='enrolls', verbose_name=b'\xd1\x83\xd1\x80\xd0\xbe\xd0\xba', blank=True, to='quizy.Lesson', null=True)),
            ],
            options={
                'verbose_name': '\u041d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435',
                'verbose_name_plural': '\u041d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(default=b'radio', max_length=10, verbose_name=b'\xd1\x82\xd0\xb8\xd0\xbf \xd0\xb2\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81\xd0\xb0', choices=[(b'radiobox', b'\xd0\x92\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81 \xd1\x81 \xd0\xb2\xd1\x8b\xd0\xb1\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbc \xd0\xbe\xd0\xb4\xd0\xbd\xd0\xbe\xd0\xb3\xd0\xbe \xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82\xd0\xb0'), (b'checkbox', b'\xd0\x92\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81 \xd1\x81 \xd0\xb2\xd1\x8b\xd0\xb1\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbc \xd0\xbd\xd0\xb5\xd1\x81\xd0\xba\xd0\xbe\xd0\xbb\xd1\x8c\xd0\xba\xd0\xb8\xd1\x85 \xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82\xd0\xbe\xd0\xb2'), (b'text', b'\xd0\xa2\xd0\xb5\xd0\xba\xd1\x81\xd1\x82\xd0\xbe\xd0\xb2\xd1\x8b\xd0\xb9 \xd0\xb2\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81'), (b'pairs', b'\xd0\x92\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81 \xd1\x81 \xd0\xbf\xd0\xbe\xd0\xb4\xd0\xb1\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbc \xd0\xbf\xd0\xb0\xd1\x80\xd1\x8b')])),
                ('text', models.TextField(null=True, verbose_name=b'\xd0\x92\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81', blank=True)),
                ('number', models.IntegerField(default=1, null=True, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x80\xd1\x8f\xd0\xb4\xd0\xbe\xd0\xba', blank=True)),
                ('is_correct', models.BooleanField(default=True, verbose_name=b'\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c \xd0\xb7\xd0\xb0\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xb2\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81\xd0\xb0')),
                ('code_errors', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name=b'\xd0\xba\xd0\xbe\xd0\xb4\xd1\x8b \xd0\xbe\xd1\x88\xd0\xb8\xd0\xb1\xd0\xbe\xd0\xba', blank=True)),
                ('lesson', models.ForeignKey(related_query_name=b'page', related_name='pages', editable=False, to='quizy.Lesson', verbose_name=b'\xd0\xba\xd1\x83\xd1\x80\xd1\x81')),
            ],
            options={
                'ordering': ('number', 'created_at', 'text'),
                'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430',
                'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b',
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(null=True, verbose_name=b'\xd1\x82\xd0\xb5\xd0\xba\xd1\x81\xd1\x82 \xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82\xd0\xb0', blank=True)),
                ('pair_type', models.CharField(default=b'question', max_length=10, verbose_name=b'\xd1\x82\xd0\xb8\xd0\xbf \xd0\xbf\xd0\xb0\xd1\x80\xd1\x8b', choices=[(b'question', b'\xd0\xb2\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81'), (b'answer', b'\xd0\xbe\xd1\x82\xd0\xb2\xd0\xb5\xd1\x82')])),
                ('right_answer', models.BooleanField(default=False)),
                ('number', models.IntegerField(default=1, verbose_name=b'\xd0\x9f\xd0\xbe\xd1\x80\xd1\x8f\xd0\xb4\xd0\xbe\xd0\xba')),
                ('is_correct', models.BooleanField(default=True, verbose_name=b'\xd0\xbf\xd1\x80\xd0\xb0\xd0\xb2\xd0\xb8\xd0\xbb\xd1\x8c\xd0\xbd\xd0\xbe\xd1\x81\xd1\x82\xd1\x8c \xd0\xb7\xd0\xb0\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xb2\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81\xd0\xb0')),
                ('code_errors', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name=b'\xd0\xba\xd0\xbe\xd0\xb4\xd1\x8b \xd0\xbe\xd1\x88\xd0\xb8\xd0\xb1\xd0\xbe\xd0\xba', blank=True)),
                ('page', models.ForeignKey(related_name='variants', to='quizy.Page')),
                ('pair', models.ForeignKey(verbose_name=b'\xd0\xbf\xd0\xb0\xd1\x80\xd0\xb0', blank=True, to='quizy.Variant', null=True)),
            ],
            options={
                'ordering': ('number', 'created_at', 'text'),
                'verbose_name': '\u041e\u0442\u0432\u0435\u0442',
                'verbose_name_plural': '\u041e\u0442\u0432\u0435\u0442\u044b',
            },
        ),
        migrations.AddField(
            model_name='attempt',
            name='enroll',
            field=models.ForeignKey(related_query_name=b'attempt', related_name='attempts', default=0, to='quizy.LessonEnroll'),
        ),
    ]
