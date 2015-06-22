# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonenroll',
            name='number_of_attempt',
            field=models.IntegerField(default=0, verbose_name=b'\xd0\xba\xd0\xbe\xd0\xbb\xd0\xb8-\xd0\xb2\xd0\xbe \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xbe\xd0\xba'),
        ),
    ]
