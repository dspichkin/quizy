# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0013_auto_20150718_2310'),
    ]

    operations = [
        migrations.RenameField(
            model_name='page',
            old_name='question_picture',
            new_name='picture',
        ),
    ]
