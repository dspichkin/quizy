# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0011_auto_20150810_1725'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lessonenroll',
            name='required_attention',
        ),
        migrations.AddField(
            model_name='lessonenroll',
            name='required_attention_by_pupil',
            field=models.NullBooleanField(verbose_name=b'\xd1\x82\xd1\x80\xd0\xb5\xd0\xb1\xd1\x83\xd0\xb5\xd1\x82\xd1\x81\xd1\x8f \xd0\xb2\xd0\xbd\xd0\xb8\xd0\xbc\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x81\xd0\xbe \xd1\x81\xd1\x82\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbd\xd1\x8b \xd1\x81\xd1\x82\xd1\x83\xd0\xb4\xd0\xb5\xd0\xbd\xd1\x82\xd0\xb0'),
        ),
        migrations.AddField(
            model_name='lessonenroll',
            name='required_attention_by_teacher',
            field=models.NullBooleanField(verbose_name=b'\xd1\x82\xd1\x80\xd0\xb5\xd0\xb1\xd1\x83\xd0\xb5\xd1\x82\xd1\x81\xd1\x8f \xd0\xb2\xd0\xbd\xd0\xb8\xd0\xbc\xd0\xb0\xd0\xbd\xd0\xb8\xd0\xb5 \xd1\x81\xd0\xbe \xd1\x81\xd1\x82\xd0\xbe\xd1\x80\xd0\xbe\xd0\xbd\xd1\x8b \xd0\xbf\xd1\x80\xd0\xb5\xd0\xbf\xd0\xbe\xd0\xb4\xd0\xbe\xd0\xb2\xd0\xb0\xd1\x82\xd0\xb5\xd0\xbb\xd1\x8f'),
        ),
    ]
