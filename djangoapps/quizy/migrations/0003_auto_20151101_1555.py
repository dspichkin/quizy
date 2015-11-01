# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings
import quizy.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizy', '0002_auto_20151022_2329'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonenroll',
            name='teacher',
            field=models.ManyToManyField(related_name='lesson_enrolls_teachers', null=True, verbose_name='\u043f\u0440\u0435\u043f\u043e\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL, blank=True),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name='\u043c\u0435\u0434\u0438\u0430 \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
    ]
