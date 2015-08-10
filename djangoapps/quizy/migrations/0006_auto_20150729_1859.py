# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0005_auto_20150727_2214'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='statistic',
            options={'verbose_name': '\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430', 'verbose_name_plural': '\u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430'},
        ),
        migrations.RenameField(
            model_name='lessonenroll',
            old_name='date_archive',
            new_name='date_success',
        ),
        migrations.RemoveField(
            model_name='lessonenroll',
            name='is_archive',
        ),
    ]
