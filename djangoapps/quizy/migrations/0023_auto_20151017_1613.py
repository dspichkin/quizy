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
        ('quizy', '0022_auto_20151017_0022'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variant',
            options={'ordering': ('number', 'created_at', 'text'), 'verbose_name': 'Answer', 'verbose_name_plural': 'Answers'},
        ),
        migrations.AlterField(
            model_name='course',
            name='code_errors',
            field=json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u043e\u0448\u0438\u0431\u043a\u0438 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='created_by',
            field=models.ForeignKey(related_name='courses', verbose_name='\u0441\u043e\u0437\u0434\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='description',
            field=models.TextField(verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u0430\u043a\u0442\u0438\u0432\u0435\u043d?'),
        ),
        migrations.AlterField(
            model_name='course',
            name='is_correct',
            field=models.BooleanField(default=True, verbose_name='\u0443\u0440\u043e\u043a \u0441\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d \u0432\u0435\u0440\u043d\u043e?'),
        ),
        migrations.AlterField(
            model_name='course',
            name='name',
            field=models.CharField(max_length=140, null=True, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u043a\u0443\u0440\u0441\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='course',
            name='teacher',
            field=models.ManyToManyField(related_name='courses_teachers', null=True, verbose_name='\u043f\u0440\u0435\u043f\u043e\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='auto_enroll',
            field=models.BooleanField(default=False, verbose_name='\u0430\u0432\u0442\u043e \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u044f \u043d\u0430 \u0443\u0440\u043e\u043a\u0438'),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='course',
            field=models.ForeignKey(related_name='course_enrolls', verbose_name='\u043a\u0443\u0440\u0441', blank=True, to='quizy.Course', null=True),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='created_by',
            field=models.ForeignKey(related_name='course_enrolls_created', verbose_name='\u043a\u0442\u043e \u0441\u043e\u0437\u0434\u0430\u043b \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='data',
            field=json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u0434\u0430\u043d\u043d\u044b\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='date_archive',
            field=models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u043f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u0438\u044f \u0432 \u0430\u0440\u0445\u0438\u0432\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='is_archive',
            field=models.BooleanField(default=False, verbose_name='\u0443\u0440\u043e\u043a \u0432 \u0430\u0440\u0445\u0438\u0432\u0435'),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='last_data',
            field=models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='learner',
            field=models.ForeignKey(related_name='course_enrolls', verbose_name='\u043e\u0431\u0443\u0447\u0430\u0435\u043c\u044b\u0439', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='number_of_attempt',
            field=models.IntegerField(default=0, verbose_name='\u043a\u043e\u043b-\u0432\u043e \u043f\u043e\u043f\u044b\u0442\u043e\u043a'),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='success',
            field=models.NullBooleanField(verbose_name='\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='code_errors',
            field=json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u043e\u0448\u0438\u0431\u043a\u0438 \u0440\u0435\u0434\u0430\u043a\u0442\u0438\u0440\u043e\u0432\u0430\u043d\u0438\u044f \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='course',
            field=models.ForeignKey(verbose_name='\u043a\u0443\u0440\u0441', blank=True, to='quizy.Course', null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='created_by',
            field=models.ForeignKey(related_name='lessons', verbose_name='\u0441\u043e\u0437\u0434\u0430\u0442\u0435\u043b\u044c', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='description',
            field=models.TextField(verbose_name='\u043e\u043f\u0438\u0441\u0430\u043d\u0438\u0435', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='full_lesson_type',
            field=models.IntegerField(verbose_name='\u0442\u0438\u043f \u0443\u0440\u043e\u043a\u0430', choices=[(1, '\u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439 \u0443\u0440\u043e\u043a'), (2, '\u0443\u0440\u043e\u043a \u043d\u0430 \u043d\u0430\u043f\u0438\u0441\u0430\u043d\u0438\u0435 \u043f\u0438\u0441\u0435\u043c')]),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='\u0430\u043a\u0442\u0438\u0432\u0435\u043d?'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='is_correct',
            field=models.BooleanField(default=True, verbose_name='\u0443\u0440\u043e\u043a \u0441\u043e\u0441\u0442\u0430\u0432\u043b\u0435\u043d \u0432\u0435\u0440\u043d\u043e?'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='\u043e\u043f\u0443\u0431\u043b\u0438\u043a\u043e\u0432\u0430\u0442\u044c \u0434\u043b\u044f \u0432\u0441\u0435\u0445'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='lesson_type',
            field=models.CharField(default=b'inside', max_length=10, verbose_name='\u0442\u0438\u043f \u0443\u0440\u043e\u043a\u0430', choices=[(b'inside', '\u0432\u043d\u0443\u0442\u0440\u0435\u043d\u043d\u0438\u0439'), (b'outside', '\u0432\u043d\u0435\u0448\u043d\u0438\u0439')]),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name='\u043c\u0435\u0434\u0438\u0430 \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='name',
            field=models.CharField(max_length=140, null=True, verbose_name='\u043d\u0430\u0437\u0432\u0430\u043d\u0438\u0435 \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='number',
            field=models.IntegerField(default=0, verbose_name='\u043f\u043e\u0440\u044f\u0434\u043e\u043a \u0441\u043b\u0435\u0434\u043e\u0432\u0430\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='path_content',
            field=models.CharField(max_length=255, null=True, verbose_name='\u043f\u0443\u0442\u044c \u043a \u043a\u043e\u043d\u0442\u0435\u043d\u0442\u0443', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='picture',
            field=sorl.thumbnail.fields.ImageField(upload_to=quizy.models.lesson_picture_upload, null=True, verbose_name='\u043a\u0430\u0440\u0442\u0438\u043d\u043a\u0430 \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='teacher',
            field=models.ManyToManyField(related_name='lessons_teachers', null=True, verbose_name='\u043f\u0440\u0435\u043f\u043e\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='timer',
            field=models.IntegerField(null=True, verbose_name='\u0442\u0430\u0439\u043c\u0435\u0440 \u0443\u0440\u043e\u043a\u0430 (\u0441\u0435\u043a)', blank=True),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='created_by',
            field=models.ForeignKey(related_name='lesson_enrolls_created', verbose_name='\u043a\u0442\u043e \u0441\u043e\u0437\u0434\u0430\u043b \u043d\u0430\u0437\u043d\u0430\u0447\u0435\u043d\u0438\u0435', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='data',
            field=json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='date_success',
            field=models.DateTimeField(null=True, verbose_name='\u0434\u0430\u0442\u0430 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u0443\u0441\u043f\u0435\u0448\u043d\u043e\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='learner',
            field=models.ForeignKey(related_name='lesson_enrolls', verbose_name='\u043e\u0431\u0443\u0447\u0430\u0435\u043c\u044b\u0439', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='lesson',
            field=models.ForeignKey(related_name='enrolls', verbose_name='\u0443\u0440\u043e\u043a', blank=True, to='quizy.Lesson', null=True),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='number_of_attempt',
            field=models.IntegerField(default=0, verbose_name='\u043a\u043e\u043b-\u0432\u043e \u043f\u043e\u043f\u044b\u0442\u043e\u043a'),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='required_attention_by_pupil',
            field=models.NullBooleanField(verbose_name='\u0442\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044f \u0432\u043d\u0438\u043c\u0430\u043d\u0438\u0435 \u0441\u043e \u0441\u0442\u043e\u0440\u043e\u043d\u044b \u0441\u0442\u0443\u0434\u0435\u043d\u0442\u0430'),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='required_attention_by_teacher',
            field=models.NullBooleanField(verbose_name='\u0442\u0440\u0435\u0431\u0443\u0435\u0442\u0441\u044f \u0432\u043d\u0438\u043c\u0430\u043d\u0438\u0435 \u0441\u043e \u0441\u0442\u043e\u0440\u043e\u043d\u044b \u043f\u0440\u0435\u043f\u043e\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044f'),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='success',
            field=models.NullBooleanField(verbose_name='\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='page',
            name='code_errors',
            field=json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u043a\u043e\u0434\u044b \u043e\u0448\u0438\u0431\u043e\u043a', blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='is_correct',
            field=models.BooleanField(default=True, verbose_name='\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0432\u043e\u043f\u0440\u043e\u0441\u0430'),
        ),
        migrations.AlterField(
            model_name='page',
            name='lesson',
            field=models.ForeignKey(related_query_name=b'page', related_name='pages', editable=False, to='quizy.Lesson', verbose_name='\u043a\u0443\u0440\u0441'),
        ),
        migrations.AlterField(
            model_name='page',
            name='number',
            field=models.IntegerField(default=1, null=True, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a', blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='text',
            field=models.TextField(null=True, verbose_name='\u0412\u043e\u043f\u0440\u043e\u0441', blank=True),
        ),
        migrations.AlterField(
            model_name='page',
            name='type',
            field=models.CharField(default=b'radio', max_length=10, verbose_name='\u0442\u0438\u043f \u0432\u043e\u043f\u0440\u043e\u0441\u0430', choices=[(b'radiobox', '\u0412\u043e\u043f\u0440\u043e\u0441 \u0441 \u0432\u044b\u0431\u043e\u0440\u043e\u043c \u043e\u0434\u043d\u043e\u0433\u043e \u043e\u0442\u0432\u0435\u0442\u0430'), (b'checkbox', '\u0412\u043e\u043f\u0440\u043e\u0441 \u0441 \u0432\u044b\u0431\u043e\u0440\u043e\u043c \u043d\u0435\u0441\u043a\u043e\u043b\u044c\u043a\u0438\u0445 \u043e\u0442\u0432\u0435\u0442\u043e\u0432'), (b'text', '\u0422\u0435\u043a\u0441\u0442\u043e\u0432\u044b\u0439 \u0432\u043e\u043f\u0440\u043e\u0441'), (b'pairs', '\u0412\u043e\u043f\u0440\u043e\u0441 \u0441 \u043f\u043e\u0434\u0431\u043e\u0440\u043e\u043c \u043f\u0430\u0440\u044b'), (b'words_in_text', '\u0421\u0442\u0440\u0430\u043d\u0438\u0446\u0430 \u0441 \u043f\u043e\u0434\u0431\u043e\u0440\u043e\u043c \u0441\u043b\u043e\u0432 \u0432 \u0442\u0435\u043a\u0441\u0442\u0435')]),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='learner',
            field=models.ForeignKey(related_name='statistics', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u043e\u0431\u0443\u0447\u0430\u0435\u043c\u044b\u0439', blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='lesson',
            field=models.ForeignKey(related_name='statistics', on_delete=django.db.models.deletion.SET_NULL, verbose_name='\u0443\u0440\u043e\u043a', blank=True, to='quizy.Lesson', null=True),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='number_of_attempt',
            field=models.IntegerField(default=0, verbose_name='\u043a\u043e\u043b-\u0432\u043e \u043f\u043e\u043f\u044b\u0442\u043e\u043a'),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='reason',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name='\u043f\u0440\u0438\u0447\u0438\u043d\u0430 \u043f\u0435\u0440\u0435\u043c\u0435\u0449\u0435\u043d\u044f \u0432 \u0441\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0443', choices=[(b'success', '\u0423\u0441\u043f\u0435\u0448\u043d\u043e \u0432\u044b\u043f\u043e\u043b\u0435\u043d\u043e'), (b'reject', '\u041e\u0442\u043a\u0430\u0437\u0430\u043b\u0441\u044f \u0432\u044b\u043f\u043e\u043b\u043d\u044f\u0442\u044c'), (b'done_time', '\u0412\u0440\u0435\u043c\u044f \u0432\u044b\u0448\u043b\u043e'), (b'not_done', '\u041d\u0435 \u043f\u0440\u0438\u0441\u0442\u0443\u043f\u0430\u043b')]),
        ),
        migrations.AlterField(
            model_name='statistic',
            name='success',
            field=models.NullBooleanField(verbose_name='\u0440\u0435\u0437\u0443\u043b\u044c\u0442\u0430\u0442 \u043f\u043e\u0441\u043b\u0435\u0434\u043d\u0435\u0439 \u043f\u043e\u043f\u044b\u0442\u043a\u0438 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='code_errors',
            field=json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u043a\u043e\u0434\u044b \u043e\u0448\u0438\u0431\u043e\u043a', blank=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='is_correct',
            field=models.BooleanField(default=True, verbose_name='\u043f\u0440\u0430\u0432\u0438\u043b\u044c\u043d\u043e\u0441\u0442\u044c \u0437\u0430\u043f\u043e\u043b\u043d\u0435\u043d\u0438\u044f \u0432\u043e\u043f\u0440\u043e\u0441\u0430'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='number',
            field=models.IntegerField(default=1, verbose_name='\u041f\u043e\u0440\u044f\u0434\u043e\u043a'),
        ),
        migrations.AlterField(
            model_name='variant',
            name='pair',
            field=models.ForeignKey(verbose_name='\u043f\u0430\u0440\u0430', blank=True, to='quizy.Variant', null=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='pair_type',
            field=models.CharField(default=b'question', max_length=10, verbose_name='\u0442\u0438\u043f \u043f\u0430\u0440\u044b', choices=[(b'question', '\u0432\u043e\u043f\u0440\u043e\u0441'), (b'answer', '\u043e\u0442\u0432\u0435\u0442')]),
        ),
        migrations.AlterField(
            model_name='variant',
            name='reflexy',
            field=models.TextField(null=True, verbose_name='\u0442\u0435\u043a\u0441\u0442 \u0440\u0435\u0444\u043b\u0435\u043a\u0441\u0438\u0438', blank=True),
        ),
        migrations.AlterField(
            model_name='variant',
            name='text',
            field=models.TextField(null=True, verbose_name='\u0442\u0435\u043a\u0441\u0442 \u043e\u0442\u0432\u0435\u0442\u0430', blank=True),
        ),
    ]
