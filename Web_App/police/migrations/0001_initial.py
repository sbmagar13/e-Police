# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Stationdata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('StationCode', models.CharField(default=b'00000000', max_length=8)),
                ('StationName', models.CharField(max_length=500)),
                ('Incharge', models.CharField(max_length=40)),
                ('State', models.CharField(max_length=50)),
                ('District', models.CharField(max_length=50)),
                ('City', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('address', models.TextField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
