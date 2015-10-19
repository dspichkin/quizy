# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import quizy.models
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0024_auto_20151017_1614'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='data',
            field=json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u0434\u0430\u043d\u043d\u044b\u0435 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='data',
            field=json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', null=True, verbose_name='\u0434\u0430\u043d\u043d\u044b\u0435 \u043f\u0440\u043e\u0445\u043e\u0436\u0434\u0435\u043d\u0438\u044f', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name='\u043c\u0435\u0434\u0438\u0430 \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
    ]
