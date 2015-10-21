# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sorl.thumbnail.fields
import django.db.models.deletion
from django.conf import settings
import quizy.models
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(unique=True, editable=False, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0430\u043a\u0442\u0438\u0432\u0435\u043d?')),
                ('name', models.CharField(max_length=140, null=True, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043a\u0443\u0440\u0441\u0430', blank=True)),
                ('description', models.TextField(verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('code_errors', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u043e\u0448\u0438\u0431\u043a\u0438 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u0443\u0440\u043e\u043a\u0430', blank=True)),
                ('is_correct', models.BooleanField(default=True, verbose_name='\u0443\u0440\u043e\u043a \u0441\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d \u0432\u0435\u0440\u043d\u043e?')),
                ('picture', sorl.thumbnail.fields.ImageField(null=True, upload_to=quizy.models.course_picture_upload, blank=True)),
                ('created_by', models.ForeignKey(related_name='courses', verbose_name='\u0441\u043e\u0437\u0434\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('teacher', models.ManyToManyField(related_name='courses_teachers', null=True, verbose_name='\u043f\u0440\u0435\u043f\u043e\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'verbose_name': '\u041a\u0443\u0440\u0441',
                'verbose_name_plural': '\u041a\u0443\u0440\u0441\u044b',
            },
        ),
        migrations.CreateModel(
            name='CourseEnroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(unique=True, editable=False, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('auto_enroll', models.BooleanField(default=False, verbose_name='\u0430\u0432\u0442\u043e \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u043d\u0430 \u0443\u0440\u043e\u043a\u0438')),
                ('data', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u0434\u0430\u043d\u043d\u044b\u0435 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True)),
                ('last_data', models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438', blank=True)),
                ('number_of_attempt', models.IntegerField(default=0, verbose_name='\u043a\u043e\u043b-\u0432\u043e \u043f\u043e\u043f\u044b\u0442\u043e\u043a')),
                ('success', models.NullBooleanField(verbose_name='\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f')),
                ('is_archive', models.BooleanField(default=False, verbose_name='\u0443\u0440\u043e\u043a \u0432 \u0430\u0440\u0445\u0438\u0432\u0435')),
                ('date_archive', models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u043f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u0438\u044f \u0432 \u0430\u0440\u0445\u0438\u0432\u0435', blank=True)),
                ('course', models.ForeignKey(related_name='course_enrolls', verbose_name='\u043a\u0443\u0440\u0441', blank=True, to='quizy.Course', null=True)),
                ('created_by', models.ForeignKey(related_name='course_enrolls_created', verbose_name='\u043a\u0442\u043e \u0441\u043e\u0437\u0434\u0430\u043b \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', to=settings.AUTH_USER_MODEL)),
                ('learner', models.ForeignKey(related_name='course_enrolls', verbose_name='\u043e\u0431\u0443\u0447\u0430\u0435\u043c\u044b\u0439', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '\u041d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043d\u0430 \u043a\u0443\u0440\u0441',
                'verbose_name_plural': '\u041d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u043d\u0430 \u043a\u0443\u0440\u0441\u044b',
            },
        ),
        migrations.CreateModel(
            name='Lesson',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(unique=True, editable=False, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('is_active', models.BooleanField(default=True, verbose_name='\u0430\u043a\u0442\u0438\u0432\u0435\u043d?')),
                ('is_public', models.BooleanField(default=False, verbose_name='\u043e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u0442\u044c \u0434\u043b\u044f \u0432\u0441\u0435\u0445')),
                ('name', models.CharField(max_length=140, null=True, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0443\u0440\u043e\u043a\u0430', blank=True)),
                ('number', models.IntegerField(default=0, verbose_name='\u043f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u044f')),
                ('description', models.TextField(verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True)),
                ('code_errors', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u043e\u0448\u0438\u0431\u043a\u0438 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u0443\u0440\u043e\u043a\u0430', blank=True)),
                ('is_correct', models.BooleanField(default=True, verbose_name='\u0443\u0440\u043e\u043a \u0441\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d \u0432\u0435\u0440\u043d\u043e?')),
                ('picture', sorl.thumbnail.fields.ImageField(upload_to=quizy.models.lesson_picture_upload, null=True, verbose_name='\u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0430 \u0443\u0440\u043e\u043a\u0430', blank=True)),
                ('lesson_type', models.CharField(default=b'inside', max_length=10, verbose_name='\u0442\u0438\u043f \u0443\u0440\u043e\u043a\u0430', choices=[(b'inside', '\u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439'), (b'outside', '\u0432\u043d\u0435\u0448\u043d\u0438\u0439')])),
                ('full_lesson_type', models.IntegerField(verbose_name='\u0442\u0438\u043f \u0443\u0440\u043e\u043a\u0430', choices=[(1, '\u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 \u0443\u0440\u043e\u043a'), (2, '\u0443\u0440\u043e\u043a \u043d\u0430 \u043d\u0430\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u0438\u0441\u0435\u043c')])),
                ('path_content', models.CharField(max_length=255, null=True, verbose_name='\u043f\u0443\u0442\u044c \u043a \u043a\u043e\u043d\u0442\u0435\u043d\u0442\u0443', blank=True)),
                ('media', models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name='\u043c\u0435\u0434\u0438\u0430 \u0443\u0440\u043e\u043a\u0430', blank=True)),
                ('timer', models.IntegerField(null=True, verbose_name='\u0442\u0430\u0439\u043c\u0435\u0440 \u0443\u0440\u043e\u043a\u0430 (\u0441\u0435\u043a)', blank=True)),
                ('course', models.ForeignKey(verbose_name='\u043a\u0443\u0440\u0441', blank=True, to='quizy.Course', null=True)),
                ('created_by', models.ForeignKey(related_name='lessons', verbose_name='\u0441\u043e\u0437\u0434\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('teacher', models.ManyToManyField(related_name='lessons_teachers', null=True, verbose_name='\u043f\u0440\u0435\u043f\u043e\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ('number',),
                'verbose_name': '\u0423\u0440\u043e\u043a',
                'verbose_name_plural': '\u0423\u0440\u043e\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='LessonEnroll',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uuid', models.UUIDField(unique=True, editable=False, db_index=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('data', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True)),
                ('number_of_attempt', models.IntegerField(default=0, verbose_name='\u043a\u043e\u043b-\u0432\u043e \u043f\u043e\u043f\u044b\u0442\u043e\u043a')),
                ('success', models.NullBooleanField(verbose_name='\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f')),
                ('date_success', models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u0443\u0441\u043f\u0435\u0448\u043d\u043e\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438', blank=True)),
                ('required_attention_by_teacher', models.NullBooleanField(verbose_name='\u0442\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044f \u0432\u043d\u0438\u043c\u0430\u043d\u0438\u0435 \u0441\u043e \u0441\u0442\u043e\u0440\u043e\u043d\u044b \u043f\u0440\u0435\u043f\u043e\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044f')),
                ('required_attention_by_pupil', models.NullBooleanField(verbose_name='\u0442\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044f \u0432\u043d\u0438\u043c\u0430\u043d\u0438\u0435 \u0441\u043e \u0441\u0442\u043e\u0440\u043e\u043d\u044b \u0441\u0442\u0443\u0434\u0435\u043d\u0442\u0430')),
                ('created_by', models.ForeignKey(related_name='lesson_enrolls_created', verbose_name='\u043a\u0442\u043e \u0441\u043e\u0437\u0434\u0430\u043b \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', to=settings.AUTH_USER_MODEL)),
                ('learner', models.ForeignKey(related_name='lesson_enrolls', verbose_name='\u043e\u0431\u0443\u0447\u0430\u0435\u043c\u044b\u0439', to=settings.AUTH_USER_MODEL)),
                ('lesson', models.ForeignKey(related_name='enrolls', verbose_name='\u0443\u0440\u043e\u043a', blank=True, to='quizy.Lesson', null=True)),
            ],
            options={
                'verbose_name': '\u041d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435 \u043d\u0430 \u0443\u0440\u043e\u043a',
                'verbose_name_plural': '\u041d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u043d\u0430 \u0443\u0440\u043e\u043a\u0438',
            },
        ),
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('type', models.CharField(default=b'radio', max_length=10, verbose_name='\u0442\u0438\u043f \u0432\u043e\u043f\u0440\u043e\u0441\u0430', choices=[(b'radiobox', '\u0412\u043e\u043f\u0440\u043e\u0441 \u0441 \u0432\u044b\u0431\u043e\u0440\u043e\u043c \u043e\u0434\u043d\u043e\u0433\u043e \u043e\u0442\u0432\u0435\u0442\u0430'), (b'checkbox', '\u0412\u043e\u043f\u0440\u043e\u0441 \u0441 \u0432\u044b\u0431\u043e\u0440\u043e\u043c \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u0438\u0445 \u043e\u0442\u0432\u0435\u0442\u043e\u0432'), (b'text', '\u0422\u0435\u043a\u0441\u0442\u043e\u0432\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441'), (b'pairs', '\u0412\u043e\u043f\u0440\u043e\u0441 \u0441 \u043f\u043e\u0434\u0431\u043e\u0440\u043e\u043c \u043f\u0430\u0440\u044b'), (b'words_in_text', '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u0441 \u043f\u043e\u0434\u0431\u043e\u0440\u043e\u043c \u0441\u043b\u043e\u0432 \u0432 \u0442\u0435\u043a\u0441\u0442\u0435')])),
                ('text', models.TextField(null=True, verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441', blank=True)),
                ('number', models.IntegerField(default=1, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a', blank=True)),
                ('media', models.FileField(null=True, upload_to=quizy.models.media_question_upload, blank=True)),
                ('is_correct', models.BooleanField(default=True, verbose_name='\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0432\u043e\u043f\u0440\u043e\u0441\u0430')),
                ('code_errors', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u043a\u043e\u0434\u044b \u043e\u0448\u0438\u0431\u043e\u043a', blank=True)),
                ('lesson', models.ForeignKey(related_query_name=b'page', related_name='pages', editable=False, to='quizy.Lesson', verbose_name='\u043a\u0443\u0440\u0441')),
            ],
            options={
                'ordering': ('number', 'created_at', 'text'),
                'verbose_name': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430',
                'verbose_name_plural': '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u044b',
            },
        ),
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('number_of_attempt', models.IntegerField(default=0, verbose_name='\u043a\u043e\u043b-\u0432\u043e \u043f\u043e\u043f\u044b\u0442\u043e\u043a')),
                ('success', models.NullBooleanField(verbose_name='\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f')),
                ('reason', models.CharField(blank=True, max_length=10, null=True, verbose_name='\u043f\u0440\u0438\u0447\u0438\u043d\u0430 \u043f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u044f \u0432 \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0443', choices=[(b'success', '\u0423\u0441\u043f\u0435\u0448\u043d\u043e \u0432\u044b\u043f\u043e\u043b\u0435\u043d\u043e'), (b'reject', '\u041e\u0442\u043a\u0430\u0437\u0430\u043b\u0441\u044f \u0432\u044b\u043f\u043e\u043b\u043d\u044f\u0442\u044c'), (b'done_time', '\u0412\u0440\u0435\u043c\u044f \u0432\u044b\u0448\u043b\u043e'), (b'not_done', '\u041d\u0435 \u043f\u0440\u0438\u0441\u0442\u0443\u043f\u0430\u043b')])),
                ('data', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u0434\u0430\u043d\u043d\u044b\u0435 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True)),
                ('learner', models.ForeignKey(related_name='statistics', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u043e\u0431\u0443\u0447\u0430\u0435\u043c\u044b\u0439', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('lesson', models.ForeignKey(related_name='statistics', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0443\u0440\u043e\u043a', blank=True, to='quizy.Lesson', null=True)),
            ],
            options={
                'ordering': ('-updated_at', '-created_at'),
                'verbose_name': '\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430/\u0410\u0440\u0445\u0438\u0432',
                'verbose_name_plural': '\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430/\u0410\u0440\u0445\u0438\u0432',
            },
        ),
        migrations.CreateModel(
            name='Variant',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('text', models.TextField(null=True, verbose_name='\u0442\u0435\u043a\u0441\u0442 \u043e\u0442\u0432\u0435\u0442\u0430', blank=True)),
                ('pair_type', models.CharField(default=b'question', max_length=10, verbose_name='\u0442\u0438\u043f \u043f\u0430\u0440\u044b', choices=[(b'question', '\u0432\u043e\u043f\u0440\u043e\u0441'), (b'answer', '\u043e\u0442\u0432\u0435\u0442')])),
                ('right_answer', models.BooleanField(default=False)),
                ('number', models.IntegerField(default=1, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a')),
                ('is_correct', models.BooleanField(default=True, verbose_name='\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0432\u043e\u043f\u0440\u043e\u0441\u0430')),
                ('code_errors', json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u043a\u043e\u0434\u044b \u043e\u0448\u0438\u0431\u043e\u043a', blank=True)),
                ('reflexy', models.TextField(null=True, verbose_name='\u0442\u0435\u043a\u0441\u0442 \u0440\u0435\u0444\u043b\u0435\u043a\u0441\u0438\u0438', blank=True)),
                ('page', models.ForeignKey(related_name='variants', to='quizy.Page')),
                ('pair', models.ForeignKey(verbose_name='\u043f\u0430\u0440\u0430', blank=True, to='quizy.Variant', null=True)),
            ],
            options={
                'ordering': ('number', 'created_at', 'text'),
                'verbose_name': '\u041e\u0442\u0432\u0435\u0442',
                'verbose_name_plural': '\u041e\u0442\u0432\u0435\u0442\u044b',
            },
        ),
    ]
