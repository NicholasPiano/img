# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('img', '__first__'),
        ('expt', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cell',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='cells')),
                ('series', models.ForeignKey(to='expt.Series', related_name='cells')),
            ],
        ),
        migrations.CreateModel(
            name='CellInstance',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('gray_value', models.IntegerField(default=0)),
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
                ('cell', models.ForeignKey(to='cell.Cell', related_name='cell_instances')),
                ('cell_instance', models.ForeignKey(null=True, related_name='cell_instances', to='cell.CellInstance')),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='cell_instances')),
                ('gon', models.OneToOneField(null=True, related_name='cell_instance', to='img.Gon')),
            ],
        ),
        migrations.CreateModel(
            name='Marker',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('r', models.IntegerField(default=0)),
                ('c', models.IntegerField(default=0)),
                ('z', models.IntegerField(default=0)),
                ('t', models.IntegerField(default=0)),
                ('channel', models.ForeignKey(to='img.Channel', related_name='markers')),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='markers')),
                ('marker', models.ForeignKey(null=True, related_name='markers', to='cell.Marker')),
                ('region', models.ForeignKey(null=True, related_name='markers', to='expt.Region')),
                ('series', models.ForeignKey(to='expt.Series', related_name='markers')),
            ],
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('track_id', models.IntegerField(default=0)),
                ('index', models.IntegerField(default=0)),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='tracks')),
                ('series', models.ForeignKey(to='expt.Series', related_name='tracks')),
            ],
        ),
        migrations.AddField(
            model_name='marker',
            name='track',
            field=models.ForeignKey(to='cell.Track', related_name='markers'),
        ),
        migrations.AddField(
            model_name='cellinstance',
            name='marker',
            field=models.OneToOneField(related_name='cell_instance_marker', to='cell.Marker'),
        ),
        migrations.AddField(
            model_name='cellinstance',
            name='region',
            field=models.ForeignKey(null=True, related_name='cell_instances', to='expt.Region'),
        ),
        migrations.AddField(
            model_name='cellinstance',
            name='series',
            field=models.ForeignKey(to='expt.Series', related_name='cell_instances'),
        ),
        migrations.AddField(
            model_name='cell',
            name='track',
            field=models.OneToOneField(related_name='cell', to='cell.Track'),
        ),
    ]
