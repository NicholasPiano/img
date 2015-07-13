# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('base_path', models.CharField(max_length=255)),
                ('img_path', models.CharField(max_length=255)),
                ('tracking_path', models.CharField(max_length=255)),
                ('composite_path', models.CharField(max_length=255)),
                ('region_path', models.CharField(max_length=255)),
                ('cp_path', models.CharField(max_length=255)),
                ('output_path', models.CharField(max_length=255)),
                ('plot_path', models.CharField(max_length=255)),
                ('track_path', models.CharField(max_length=255)),
                ('data_path', models.CharField(max_length=255)),
                ('pipeline_path', models.CharField(max_length=255)),
                ('rmop', models.FloatField(default=0.0)),
                ('cmop', models.FloatField(default=0.0)),
                ('zmop', models.FloatField(default=0.0)),
                ('tpf', models.FloatField(default=0.0)),
            ],
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('t', models.IntegerField(default=0)),
                ('z', models.IntegerField(default=0)),
                ('channel', models.ForeignKey(to='expt.Channel', related_name='paths')),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='paths')),
            ],
        ),
        migrations.CreateModel(
            name='Region',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('index', models.IntegerField(default=0)),
                ('vertical_sort_index', models.IntegerField(default=0)),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='regions')),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rs', models.IntegerField(default=-1)),
                ('cs', models.IntegerField(default=-1)),
                ('zs', models.IntegerField(default=-1)),
                ('ts', models.IntegerField(default=-1)),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='series')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('rx', models.CharField(max_length=255)),
                ('rv', models.CharField(max_length=255)),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='templates')),
            ],
        ),
        migrations.AddField(
            model_name='region',
            name='series',
            field=models.ForeignKey(to='expt.Series', related_name='regions'),
        ),
        migrations.AddField(
            model_name='path',
            name='series',
            field=models.ForeignKey(to='expt.Series', related_name='paths'),
        ),
        migrations.AddField(
            model_name='path',
            name='template',
            field=models.ForeignKey(to='expt.Template', related_name='paths'),
        ),
        migrations.AddField(
            model_name='channel',
            name='experiment',
            field=models.ForeignKey(to='expt.Experiment', related_name='channels'),
        ),
    ]
