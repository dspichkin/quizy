# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0003_auto_20150620_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonenroll',
            name='is_passed',
            field=models.BooleanField(default=False, verbose_name=b'\xd0\xb1\xd1\x8b\xd0\xbb\xd0\xb0 \xd0\xbb\xd0\xb8 \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xba\xd0\xb0 \xd0\xbf\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb6\xd0\xb4\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f?'),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='number_of_attempt',
            field=models.IntegerField(default=0, verbose_name=b'\xd0\xba\xd0\xbe\xd0\xbb-\xd0\xb2\xd0\xbe \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xbe\xd0\xba'),
        ),
        migrations.AlterField(
            model_name='lessonenroll',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name=b'\xd0\xbf\xd0\xbe\xd1\x81\xd0\xbb\xd0\xb5\xd0\xb4\xd0\xbd\xd1\x8f\xd1\x8f \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xba\xd0\xb0'),
        ),
    ]
