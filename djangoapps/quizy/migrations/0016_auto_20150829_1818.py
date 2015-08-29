# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import quizy.models


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0015_auto_20150829_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='uuid',
            field=models.UUIDField(unique=True, editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='courseenroll',
            name='uuid',
            field=models.UUIDField(unique=True, editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name=b'\xd0\xbc\xd0\xb5\xd0\xb4\xd0\xb8\xd0\xb0 \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0', blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='uuid',
            field=models.UUIDField(unique=True, editable=False, db_index=True),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='uuid',
            field=models.UUIDField(unique=True, editable=False, db_index=True),
        ),
    ]
