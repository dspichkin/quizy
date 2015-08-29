# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import quizy.models


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0016_auto_20150829_1818'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='full_lesson_type',
            field=models.CharField(default=b'inside', max_length=10, verbose_name=b'\xd1\x82\xd0\xb8\xd0\xbf \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0', choices=[(b'1', b'\xd0\xb2\xd0\xbd\xd1\x83\xd1\x82\xd1\x80\xd0\xb5\xd0\xbd\xd0\xbd\xd0\xb8\xd0\xb9 \xd1\x83\xd1\x80\xd0\xbe\xd0\xba'), (b'2', b'\xd1\x83\xd1\x80\xd0\xbe\xd0\xba \xd0\xbd\xd0\xb0 \xd0\xbd\xd0\xb0\xd0\xbf\xd0\xb8\xd1\x81\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd0\xbf\xd0\xb8\xd1\x81\xd1\x8c\xd0\xbc\xd0\xb0')]),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name=b'\xd0\xbc\xd0\xb5\xd0\xb4\xd0\xb8\xd0\xb0 \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0', blank=True),
        ),
    ]
