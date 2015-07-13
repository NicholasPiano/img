# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expt', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='cp2_path',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='mask_path',
        ),
        migrations.RemoveField(
            model_name='experiment',
            name='sub_mask_path',
        ),
    ]
