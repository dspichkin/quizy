# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quizy', '0004_auto_20150724_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='Statistic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('number_of_attempt', models.IntegerField(default=0, verbose_name=b'\xd0\xba\xd0\xbe\xd0\xbb-\xd0\xb2\xd0\xbe \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xbe\xd0\xba')),
                ('success', models.NullBooleanField(verbose_name=b'\xd1\x80\xd0\xb5\xd0\xb7\xd1\x83\xd0\xbb\xd1\x8c\xd1\x82\xd0\xb0\xd1\x82 \xd0\xbf\xd0\xbe\xd1\x81\xd0\xbb\xd0\xb5\xd0\xb4\xd0\xbd\xd0\xb5\xd0\xb9 \xd0\xbf\xd0\xbe\xd0\xbf\xd1\x8b\xd1\x82\xd0\xba\xd0\xb8 \xd0\xbf\xd1\x80\xd0\xbe\xd1\x85\xd0\xbe\xd0\xb6\xd0\xb4\xd0\xb5\xd0\xbd\xd0\xb8\xd1\x8f')),
                ('learner', models.ForeignKey(related_name='statistics', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xd0\xbe\xd0\xb1\xd1\x83\xd1\x87\xd0\xb0\xd0\xb5\xd0\xbc\xd1\x8b\xd0\xb9', blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('lesson', models.ForeignKey(related_name='statistics', on_delete=django.db.models.deletion.SET_NULL, verbose_name=b'\xd1\x83\xd1\x80\xd0\xbe\xd0\xba', blank=True, to='quizy.Lesson', null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='attempt',
            name='enroll',
        ),
        migrations.DeleteModel(
            name='Attempt',
        ),
    ]
