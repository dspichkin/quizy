# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_auto_20150716_2035'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='pupils',
            field=models.ManyToManyField(db_constraint='\u0443\u0447\u0435\u043d\u0438\u043a\u0438', to=settings.AUTH_USER_MODEL, related_name='pupils_rel_+'),
        ),
    ]
