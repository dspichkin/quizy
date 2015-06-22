# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='account_type',
            field=models.IntegerField(default=0, verbose_name='\u0442\u0438\u043f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430', choices=[(0, '\u0443\u0447\u0438\u0442\u0435\u043b\u044c'), (1, '\u0443\u0447\u0435\u043d\u0438\u043a')]),
        ),
    ]
