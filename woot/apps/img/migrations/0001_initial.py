# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('expt', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Channel',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Composite',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('id_token', models.CharField(max_length=8)),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='composites')),
                ('series', models.ForeignKey(to='expt.Series', related_name='composites')),
            ],
        ),
        migrations.CreateModel(
            name='Gon',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('id_token', models.CharField(default='', max_length=8)),
                ('batch', models.IntegerField(default=0)),
                ('r', models.IntegerField(default=0)),
                ('c', models.IntegerField(default=0)),
                ('z', models.IntegerField(default=0)),
                ('t', models.IntegerField(default=-1)),
                ('rs', models.IntegerField(default=-1)),
                ('cs', models.IntegerField(default=-1)),
                ('zs', models.IntegerField(default=1)),
                ('channel', models.ForeignKey(to='img.Channel', related_name='gons')),
                ('composite', models.ForeignKey(to='img.Composite', null=True, related_name='gons')),
                ('experiment', models.ForeignKey(to='expt.Experiment', related_name='gons')),
                ('gon', models.ForeignKey(to='img.Gon', null=True, related_name='gons')),
                ('series', models.ForeignKey(to='expt.Series', related_name='gons')),
            ],
        ),
        migrations.CreateModel(
            name='Mod',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('id_token', models.CharField(max_length=8)),
                ('algorithm', models.CharField(max_length=255)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('composite', models.ForeignKey(to='img.Composite', related_name='mods')),
            ],
        ),
        migrations.CreateModel(
            name='Path',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('url', models.CharField(max_length=255)),
                ('file_name', models.CharField(max_length=255)),
                ('t', models.IntegerField(default=0)),
                ('z', models.IntegerField(default=0)),
                ('channel', models.ForeignKey(to='img.Channel', related_name='paths')),
                ('composite', models.ForeignKey(to='img.Composite', related_name='paths')),
                ('gon', models.ForeignKey(to='img.Gon', related_name='paths')),
            ],
        ),
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('rx', models.CharField(max_length=255)),
                ('rv', models.CharField(max_length=255)),
                ('composite', models.ForeignKey(to='img.Composite', related_name='templates')),
            ],
        ),
        migrations.AddField(
            model_name='path',
            name='template',
            field=models.ForeignKey(to='img.Template', related_name='paths'),
        ),
        migrations.AddField(
            model_name='gon',
            name='template',
            field=models.ForeignKey(to='img.Template', null=True, related_name='gons'),
        ),
        migrations.AddField(
            model_name='channel',
            name='composite',
            field=models.ForeignKey(to='img.Composite', related_name='channels'),
        ),
    ]
