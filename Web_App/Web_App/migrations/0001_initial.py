# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('police', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fir',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref_id', models.CharField(default=b'00000', unique=True, max_length=40)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=80)),
                ('address', models.TextField()),
                ('DOB', models.DateField(verbose_name=b'date of birth')),
                ('idType_1', models.CharField(max_length=10)),
                ('idType_1_value', models.CharField(max_length=15)),
                ('idType_2', models.CharField(max_length=20)),
                ('idType_2_value', models.CharField(max_length=15)),
                ('Subject', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('detail', models.TextField()),
                ('Suspect', models.CharField(max_length=500)),
                ('Time', models.DateTimeField(verbose_name=b'Occurence')),
                ('Place', models.CharField(max_length=200)),
                ('Witness', models.CharField(max_length=500)),
                ('Loss', models.CharField(max_length=200)),
                ('OTP', models.BooleanField(default=False)),
                ('StationCode', models.ForeignKey(to='police.Stationdata')),
            ],
        ),
        migrations.CreateModel(
            name='general_diary',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref_id', models.CharField(default=b'00000', unique=True, max_length=40)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.CharField(max_length=80)),
                ('address', models.TextField()),
                ('DOB', models.DateField(verbose_name=b'date of birth')),
                ('idType_1', models.CharField(max_length=10)),
                ('idType_1_value', models.CharField(max_length=15)),
                ('idType_2', models.CharField(max_length=20)),
                ('idType_2_value', models.CharField(max_length=15)),
                ('Subject', models.CharField(max_length=200)),
                ('pub_date', models.DateTimeField(verbose_name=b'date published')),
                ('detail', models.TextField()),
                ('Time', models.DateTimeField(verbose_name=b'Occurence')),
                ('Place', models.CharField(max_length=200)),
                ('Loss', models.CharField(max_length=200)),
                ('OTP', models.BooleanField(default=False)),
                ('StationCode', models.ForeignKey(to='police.Stationdata')),
            ],
        ),
        migrations.CreateModel(
            name='lookup_table',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ref_id', models.CharField(default=b'00000', unique=True, max_length=40)),
                ('hashmap', models.CharField(default=b'00000', unique=True, max_length=70)),
                ('type', models.CharField(default=b'GD', max_length=5)),
            ],
        ),
    ]
