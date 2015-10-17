# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_auto_20150719_1434'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailconfirmation',
            options={'verbose_name': '\u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u0435 email \u0430\u0434\u0440\u0435\u0441\u0430', 'verbose_name_plural': '\u043f\u043e\u0434\u0442\u0432\u0435\u0440\u0436\u0434\u0435\u043d\u0438\u044f email \u0430\u0434\u0440\u0435\u0441\u043e\u0432'},
        ),
        migrations.AddField(
            model_name='account',
            name='language',
            field=models.CharField(default=b'ru', max_length=b'10', verbose_name='\u0432\u044b\u0431\u0440\u0430\u043d\u043d\u044b\u0439 \u044f\u0437\u044b\u043a \u0438\u043d\u0442\u0435\u0440\u0444\u0435\u0439\u0441\u0430', choices=[(b'ru', 'Russian'), (b'en', 'English')]),
        ),
        migrations.AlterField(
            model_name='emailconfirmation',
            name='created',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='\u0441\u043e\u0437\u0434\u0430\u043d\u043e'),
        ),
        migrations.AlterField(
            model_name='emailconfirmation',
            name='key',
            field=models.CharField(unique=True, max_length=64, verbose_name='\u043a\u043b\u044e\u0447'),
        ),
        migrations.AlterField(
            model_name='emailconfirmation',
            name='sent',
            field=models.DateTimeField(null=True, verbose_name='\u043e\u0442\u043f\u0440\u0430\u0432\u043b\u0435\u043d\u043e'),
        ),
        migrations.AlterField(
            model_name='emailconfirmation',
            name='user',
            field=models.ForeignKey(verbose_name='\u043f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u044c', to=settings.AUTH_USER_MODEL),
        ),
    ]
