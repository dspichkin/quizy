# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0002_lessonenroll_number_of_attempt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonenroll',
            name='is_passed',
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name=b'\xd0\xbd\xd0\xb0\xd0\xb7\xd0\xbd\xd0\xb0\xd1\x87\xd0\xb5\xd0\xbd\xd0\xbe'),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name=b'\xd0\xbf\xd1\x80\xd0\xbe\xd0\xb9\xd0\xb4\xd0\xb5\xd0\xbd\xd0\xbe'),
        ),
    ]
