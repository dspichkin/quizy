# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizy', '0010_auto_20150716_1345'),
    ]

    operations = [
        migrations.AddField(
            model_name='lessonenroll',
            name='created_by',
            field=models.ForeignKey(related_name='enroll_created', default=1, verbose_name=b'\xd0\xba\xd1\x82\xd0\xbe \xd1\x81\xd0\xbe\xd0\xb7\xd0\xb4\xd0\xb0\xd0\xbb \xd0\xbd\xd0\xb0\xd0\xb7\xd0\xbd\xd0\xb0\xd1\x87\xd0\xb5\xd0\xbd\xd0\xb8\xd0\xb5', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
