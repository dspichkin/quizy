# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_systemmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='account_type',
            field=models.IntegerField(default=1, verbose_name='\u0442\u0438\u043f \u0430\u043a\u043a\u0430\u0443\u043d\u0442\u0430', choices=[(1, '\u041f\u0440\u0435\u043f\u043e\u0434\u043e\u0432\u0430\u0442\u0435\u043b\u044c'), (2, '\u0423\u0447\u0435\u043d\u0438\u043a')]),
        ),
    ]
