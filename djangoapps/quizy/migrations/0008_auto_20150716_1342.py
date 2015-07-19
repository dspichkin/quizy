# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import json_field.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0007_auto_20150716_1341'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lessonenroll',
            name='data',
            field=json_field.fields.JSONField(default={}, help_text='Enter a valid JSON object', verbose_name=b'\xd1\x80\xd0\xb5\xd0\xb7\xd1\x83\xd0\xbb\xd1\x8c\xd1\x82\xd0\xb0\xd1\x82 \xd0\xbf\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb6\xd0\xb4\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f'),
        ),
    ]
