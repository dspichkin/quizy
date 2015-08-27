# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import quizy.models


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0012_auto_20150812_1114'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name=b'\xd0\xbc\xd0\xb5\xd0\xb4\xd0\xb8\xd0\xb0 \xd0\xb2\xd0\xbe\xd0\xbf\xd1\x80\xd0\xbe\xd1\x81\xd0\xb0', blank=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='timeer',
            field=models.IntegerField(null=True, verbose_name=b'\xd1\x82\xd0\xb0\xd0\xb9\xd0\xbc\xd0\xb5\xd1\x80 \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0', blank=True),
        ),
    ]
