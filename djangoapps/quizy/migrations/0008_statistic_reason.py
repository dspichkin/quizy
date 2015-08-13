# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0007_auto_20150729_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='statistic',
            name='reason',
            field=models.CharField(blank=True, max_length=10, null=True, verbose_name=b'\xd0\xbf\xd1\x80\xd0\xb8\xd1\x87\xd0\xb8\xd0\xbd\xd0\xb0 \xd0\xbf\xd0\xb5\xd1\x80\xd0\xb5\xd0\xbc\xd0\xb5\xd1\x89\xd0\xb5\xd0\xbd\xd1\x8f \xd0\xb2 \xd1\x81\xd1\x82\xd0\xb0\xd1\x82\xd0\xb8\xd1\x81\xd1\x82\xd0\xb8\xd0\xba\xd1\x83', choices=[(b'success', b'\xd0\xa3\xd1\x81\xd0\xbf\xd0\xb5\xd1\x88\xd0\xbd\xd0\xbe \xd0\xb2\xd1\x8b\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xb5\xd0\xbd\xd0\xbe'), (b'reject', b'\xd0\x9e\xd1\x82\xd0\xba\xd0\xb0\xd0\xb7\xd0\xb0\xd0\xbb\xd1\x81\xd1\x8f \xd0\xb2\xd1\x8b\xd0\xbf\xd0\xbe\xd0\xbb\xd0\xbd\xd1\x8f\xd1\x82\xd1\x8c'), (b'done_time', b'\xd0\x92\xd1\x80\xd0\xb5\xd0\xbc\xd1\x8f \xd0\xb2\xd1\x8b\xd1\x88\xd0\xbb\xd0\xbe'), (b'not_done', b'\xd0\x9d\xd0\xb5 \xd0\xbf\xd1\x80\xd0\xb8\xd1\x81\xd1\x82\xd1\x83\xd0\xbf\xd0\xb0\xd0\xbb')]),
        ),
    ]