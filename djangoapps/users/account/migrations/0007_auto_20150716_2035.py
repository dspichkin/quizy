# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_account_pupil'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='pupil',
        ),
        migrations.AddField(
            model_name='account',
            name='pupils',
            field=models.ManyToManyField(related_name='pupils_rel_+', db_constraint='\u0443\u0447\u0435\u043d\u0438\u043a\u0438', null=True, to=settings.AUTH_USER_MODEL, blank=True),
        ),
    ]
