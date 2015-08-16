# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0009_auto_20150801_1410'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lesson',
            options={'ordering': ('number',), 'verbose_name': '\u0423\u0440\u043e\u043a', 'verbose_name_plural': '\u0423\u0440\u043e\u043a\u0438'},
        ),
        migrations.RemoveField(
            model_name='lessonenroll',
            name='course',
        ),
    ]
