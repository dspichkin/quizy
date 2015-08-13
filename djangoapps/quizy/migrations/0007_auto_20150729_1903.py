# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0006_auto_20150729_1859'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonenroll',
            name='last_data',
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='date_success',
            field=models.DateTimeField(null=True, verbose_name=b'\xd0\xb4\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbe\xd1\x81\xd0\xbb\xd0\xb5\xd0\xb4\xd0\xbd\xd0\xb5\xd0\xb9 \xd1\x83\xd1\x81\xd0\xbf\xd0\xb5\xd1\x88\xd0\xbd\xd0\xbe\xd0\xb9 \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xba\xd0\xb8', blank=True),
        ),
    ]