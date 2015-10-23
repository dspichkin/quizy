# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import quizy.models


class Migration(migrations.Migration):

    dependencies = [
        ('quizy', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=100, verbose_name='\u0418\u043c\u044f')),
                ('slug', models.SlugField(unique=True, max_length=100, verbose_name='\u0421\u043b\u0430\u0433')),
            ],
            options={
                'verbose_name': '\u041c\u0435\u0442\u043a\u0430',
                'verbose_name_plural': '\u041c\u0435\u0442\u043a\u0438',
            },
        ),
        migrations.AlterField(
            model_name='lesson',
            name='media',
            field=models.FileField(upload_to=quizy.models.media_question_upload, null=True, verbose_name='\u043c\u0435\u0434\u0438\u0430 \u0443\u0440\u043e\u043a\u0430', blank=True),
        ),
        migrations.AddField(
            model_name='lesson',
            name='tag',
            field=models.ManyToManyField(related_name='lessons_tags', null=True, verbose_name='\u043c\u0435\u0442\u043a\u0438', to='quizy.Tag', blank=True),
        ),
    ]
