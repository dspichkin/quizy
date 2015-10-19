# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import quizy.models


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0024_auto_20151017_1614'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name='\u043c\u0435\u0434\u0438\u0430 \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
    ]
