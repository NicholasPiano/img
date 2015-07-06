# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('img', '0001_initial'),
        ('expt', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('cell_id', models.IntegerField(default=0)),
                ('cell_index', models.IntegerField(default=0)),
                ('experiment', models.ForeignKey(related_name='cells', to='expt.Experiment')),
                ('series', models.ForeignKey(related_name='cells', to='expt.Series')),
            ],
        ),
        migrations.CreateModel(
            name='CellInstance',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('r', models.IntegerField(default=0)),
                ('c', models.IntegerField(default=0)),
                ('z', models.IntegerField(default=0)),
                ('t', models.IntegerField(default=0)),
                ('vr', models.IntegerField(default=0)),
                ('vc', models.IntegerField(default=0)),
                ('vz', models.IntegerField(default=0)),
                ('AreaShape_Area', models.IntegerField(default=0)),
                ('AreaShape_Compactness', models.FloatField(default=0.0)),
                ('AreaShape_Eccentricity', models.FloatField(default=0.0)),
                ('AreaShape_EulerNumber', models.FloatField(default=0.0)),
                ('AreaShape_Extent', models.FloatField(default=0.0)),
                ('AreaShape_FormFactor', models.FloatField(default=0.0)),
                ('AreaShape_MajorAxisLength', models.FloatField(default=0.0)),
                ('AreaShape_MaximumRadius', models.FloatField(default=0.0)),
                ('AreaShape_MeanRadius', models.FloatField(default=0.0)),
                ('AreaShape_MedianRadius', models.FloatField(default=0.0)),
                ('AreaShape_MinorAxisLength', models.FloatField(default=0.0)),
                ('AreaShape_Orientation', models.FloatField(default=0.0)),
                ('AreaShape_Perimeter', models.FloatField(default=0.0)),
                ('AreaShape_Solidity', models.FloatField(default=0.0)),
                ('Location_Center_X', models.FloatField(default=0.0)),
                ('Location_Center_Y', models.FloatField(default=0.0)),
                ('cell', models.ForeignKey(related_name='cell_instances', to='cell.Cell')),
                ('experiment', models.ForeignKey(related_name='cell_instances', to='expt.Experiment')),
                ('gon', models.OneToOneField(related_name='cell_instance', null=True, to='img.Gon')),
                ('region', models.ForeignKey(related_name='cell_instances', to='expt.Region', null=True)),
                ('series', models.ForeignKey(related_name='cell_instances', to='expt.Series')),
            ],
        ),
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('r', models.IntegerField(default=0)),
                ('c', models.IntegerField(default=0)),
                ('z', models.IntegerField(default=0)),
                ('t', models.IntegerField(default=0)),
                ('confidence', models.FloatField(default=0.0)),
                ('experiment', models.ForeignKey(related_name='markers', to='expt.Experiment')),
                ('gon', models.OneToOneField(related_name='marker', null=True, to='img.Gon')),
                ('region', models.ForeignKey(related_name='markers', to='expt.Region', null=True)),
                ('series', models.ForeignKey(related_name='markers', to='expt.Series')),
            ],
        ),
        migrations.CreateModel(
            name='Mask',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('mask_id', models.IntegerField(default=0)),
                ('r', models.IntegerField(default=0)),
                ('c', models.IntegerField(default=0)),
                ('z', models.IntegerField(default=0)),
                ('rs', models.IntegerField(default=-1)),
                ('cs', models.IntegerField(default=-1)),
                ('max_z', models.IntegerField(default=0)),
                ('mean', models.FloatField(default=0.0)),
                ('std', models.FloatField(default=0.0)),
                ('channel', models.ForeignKey(related_name='masks', to='img.Channel')),
                ('composite', models.ForeignKey(related_name='masks', to='img.Composite')),
                ('gon', models.ForeignKey(related_name='masks', to='img.Gon')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('track_id', models.IntegerField(default=0)),
                ('index', models.IntegerField(default=0)),
                ('experiment', models.ForeignKey(related_name='tracks', to='expt.Experiment')),
                ('series', models.ForeignKey(related_name='tracks', to='expt.Series')),
            ],
        ),
        migrations.AddField(
            model_name='marker',
            name='track',
            field=models.ForeignKey(related_name='markers', to='cell.Track'),
        ),
    ]
