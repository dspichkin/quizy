# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='code_errors',
            field=json_field.fields.JSONField(default=b'{}', help_text='Enter a valid JSON object', verbose_name=b'\xd0\xbe\xd1\x88\xd0\xb8\xd0\xb1\xd0\xba\xd0\xb8 \xd1\x80\xd0\xb5\xd0\xb4\xd0\xb0\xd0\xba\xd1\x82\xd0\xb8\xd1\x80\xd0\xbe\xd0\xb2\xd0\xb0\xd0\xbd\xd0\xb8\xd1\x8f \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0'),
        ),
        migrations.AddField(
            model_name='lesson',
            name='is_correct',
            field=models.BooleanField(default=False, verbose_name=b'\xd1\x81\xd0\xbe\xd0\xb4\xd0\xb5\xd1\x80\xd0\xb6\xd0\xb8\xd1\x82 \xd0\xbe\xd1\x88\xd0\xb8\xd0\xb1\xd0\xba\xd1\x83?'),
        ),
    ]
