# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields
import quizy.models


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0005_lesson_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='page',
            name='question_picture',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=quizy.models.picture_question_upload, blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='picture',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=quizy.models.picture_upload, blank=True),
        ),
    ]
