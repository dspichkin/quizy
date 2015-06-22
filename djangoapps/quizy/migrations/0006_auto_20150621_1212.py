# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0005_auto_20150621_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonenroll',
            name='date_archive',
            field=models.DateField(null=True, verbose_name=b'\xd0\xb4\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xb5\xd1\x80\xd0\xb5\xd0\xbc\xd0\xb5\xd1\x89\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f \xd0\xb2 \xd0\xb0\xd1\x80\xd1\x85\xd0\xb8\xd0\xb2\xd0\xb5', blank=True),
        ),
        migrations.AddField(
            model_name='lessonenroll',
            name='is_archive',
            field=models.BooleanField(default=False, verbose_name=b'\xd1\x83\xd1\x80\xd0\xbe\xd0\xba \xd0\xb2 \xd0\xb0\xd1\x80\xd1\x85\xd0\xb8\xd0\xb2\xd0\xb5'),
        ),
    ]
