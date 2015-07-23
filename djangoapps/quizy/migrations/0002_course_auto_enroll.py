# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='auto_enroll',
            field=models.BooleanField(default=False, verbose_name=b'\xd1\x82\xd0\xb8\xd0\xbf \xd0\xbd\xd0\xb0\xd0\xb7\xd0\xbd\xd0\xb0\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb9 \xd0\xbd\xd0\xb0 \xd1\x83\xd1\x80\xd0\xbe\xd0\xba\xd0\xb8'),
        ),
    ]
