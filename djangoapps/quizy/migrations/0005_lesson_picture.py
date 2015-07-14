# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import sorl.thumbnail.fields


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0004_auto_20150710_1003'),
    ]

    operations = [
        migrations.AddField(
            model_name='lesson',
            name='picture',
            field=sorl.thumbnail.fields.ImageField(null=True, upload_to=b'picture_upload', blank=True),
        ),
    ]
