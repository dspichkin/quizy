# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20150704_1309'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='pupil',
            field=models.ManyToManyField(related_name='pupil_rel_+', db_constraint='\u0443\u0447\u0435\u043d\u0438\u043a\u0438', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
