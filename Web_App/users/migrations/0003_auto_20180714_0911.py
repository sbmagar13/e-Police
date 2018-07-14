# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20180713_2240'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='AadharModel',
            new_name='CtzModel',
        ),
        migrations.RenameModel(
            old_name='PanModel',
            new_name='LcnModel',
        ),
        migrations.RenameModel(
            old_name='RationModel',
            new_name='PasModel',
        ),
        migrations.RenameField(
            model_name='ctzmodel',
            old_name='aid',
            new_name='cid',
        ),
        migrations.RenameField(
            model_name='lcnmodel',
            old_name='pid',
            new_name='lid',
        ),
        migrations.RenameField(
            model_name='pasmodel',
            old_name='rid',
            new_name='pid',
        ),
    ]
