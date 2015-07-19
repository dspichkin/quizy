# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0008_auto_20150716_1342'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonenroll',
            old_name='data',
            new_name='result',
        ),
    ]
