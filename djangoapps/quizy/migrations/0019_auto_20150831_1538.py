# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import quizy.models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0018_auto_20150829_2105'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statistic',
            options={'ordering': ('-updated_at', '-created_at'), 'verbose_name': '\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430', 'verbose_name_plural': '\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430'},
        ),
        migrations.AddField(
            model_name='statistic',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 8, 31, 12, 38, 25, 987100, tzinfo=utc), auto_now=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name=b'\xd0\xbc\xd0\xb5\xd0\xb4\xd0\xb8\xd0\xb0 \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb0', blank=True),
        ),
    ]
