# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import quizy.models


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0023_auto_20151017_1613'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='variant',
            options={'ordering': ('number', 'created_at', 'text'), 'verbose_name': '\u041e\u0442\u0432\u0435\u0442', 'verbose_name_plural': '\u041e\u0442\u0432\u0435\u0442\u044b'},
        ),
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name='\u043c\u0435\u0434\u0438\u0430 \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
    ]
