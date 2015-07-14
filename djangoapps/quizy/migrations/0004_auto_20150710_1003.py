# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0003_auto_20150710_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lesson',
            name='is_correct',
            field=models.BooleanField(default=True, verbose_name=b'\xd1\x81\xd0\xbe\xd0\xb4\xd0\xb5\xd1\x80\xd0\xb6\xd0\xb8\xd1\x82 \xd0\xbe\xd1\x88\xd0\xb8\xd0\xb1\xd0\xba\xd1\x83?'),
        ),
    ]
