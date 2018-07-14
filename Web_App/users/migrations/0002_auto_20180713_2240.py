# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AadharModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=40)),
                ('lastname', models.CharField(max_length=40)),
                ('aid', models.CharField(unique=True, max_length=15)),
                ('address', models.TextField()),
                ('dob', models.DateField(verbose_name=b'Date of Birth')),
            ],
        ),
        migrations.CreateModel(
            name='PanModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=40)),
                ('lastname', models.CharField(max_length=40)),
                ('pid', models.CharField(unique=True, max_length=15)),
                ('address', models.TextField()),
                ('dob', models.DateField(verbose_name=b'Date of Birth')),
            ],
        ),
        migrations.CreateModel(
            name='RationModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=40)),
                ('lastname', models.CharField(max_length=40)),
                ('rid', models.CharField(unique=True, max_length=15)),
                ('address', models.TextField()),
                ('dob', models.DateField(verbose_name=b'Date of Birth')),
            ],
        ),
        migrations.CreateModel(
            name='Userdata',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.CharField(unique=True, max_length=40)),
                ('firstname', models.CharField(max_length=40)),
                ('lastname', models.CharField(max_length=40)),
                ('phone', models.CharField(unique=True, max_length=10)),
                ('address', models.TextField()),
                ('dob', models.DateField(verbose_name=b'Date of Birth')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='VoterModel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('firstname', models.CharField(max_length=40)),
                ('lastname', models.CharField(max_length=40)),
                ('vid', models.CharField(unique=True, max_length=15)),
                ('address', models.TextField()),
                ('dob', models.DateField(verbose_name=b'Date of Birth')),
            ],
        ),
        migrations.DeleteModel(
            name='Fir',
        ),
        migrations.DeleteModel(
            name='General_Diary',
        ),
    ]
