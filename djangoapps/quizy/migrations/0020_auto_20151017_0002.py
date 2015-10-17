# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import quizy.models


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0019_auto_20150831_1538'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name=b'\xd0\xbe\xd0\xbf\xd1\x83\xd0\xb1\xd0\xbb\xd0\xb8\xd0\xba\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd1\x8c \xd0\xb4\xd0\xbb\xd1\x8f \xd0\xb2\xd1\x81\xd0\xb5\xd1\x85'),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name=b'\xd0\xbc\xd0\xb5\xd0\xb4\xd0\xb8\xd0\xb0 \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0', blank=True),
        ),
    ]
