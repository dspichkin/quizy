# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0008_statistic_reason'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='lesson_type',
            field=models.CharField(default=b'inside', max_length=10, verbose_name=b'\xd1\x82\xd0\xb8\xd0\xbf \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0', choices=[(b'inside', b'\xd0\xb2\xd0\xbd\xd1\x83\xd1\x82\xd1\x80\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xb8\xd0\xb9'), (b'custom', b'\xd0\xbd\xd0\xb0\xd1\x81\xd1\x82\xd1\x80\xd0\xb0\xd0\xb8\xd0\xb2\xd0\xb0\xd0\xb5\xd0\xbc\xd1\x8b\xd0\xb9')]),
        ),
        migrations.AddField(
            model_name='lesson',
            name='path_content',
            field=models.CharField(max_length=255, null=True, verbose_name=b'\xd0\xbf\xd1\x83\xd1\x82\xd1\x8c \xd0\xba \xd0\xba\xd0\xbe\xd0\xbd\xd1\x82\xd0\xb5\xd0\xbd\xd1\x82\xd1\x83', blank=True),
        ),
    ]
