# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0011_lessonenroll_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonenroll',
            name='last_data',
            field=models.DateTimeField(default=datetime.datetime(2015, 7, 18, 18, 18, 46, 274093, tzinfo=utc), verbose_name=b'\xd0\xb4\xd0\xb0\xd1\x82\xd0\xb0 \xd0\xbf\xd0\xbe\xd1\x81\xd0\xbb\xd0\xb5\xd0\xb4\xd0\xbd\xd0\xb5\xd0\xb9 \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xba\xd0\xb8', blank=True),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='lesson',
            name='is_correct',
            field=models.BooleanField(default=True, verbose_name=b'\xd1\x83\xd1\x80\xd0\xbe\xd0\xba \xd1\x81\xd0\xbe\xd1\x81\xd1\x82\xd0\xb0\xd0\xb2\xd0\xbb\xd0\xb5\xd0\xbd \xd0\xb2\xd0\xb5\xd1\x80\xd0\xbd\xd0\xbe?'),
        ),
    ]
