# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('time', models.DateTimeField(help_text='Time for the observation')),
                ('observed', models.DateTimeField(help_text='When the observation was taken (call to API)')),
                ('_non_forecast', models.BooleanField()),
                ('temperature', models.FloatField(default=0, verbose_name='temperature (\xbaC)')),
                ('ozone', models.FloatField(null=True, blank=True)),
                ('apparent_temperature', models.FloatField(null=True, blank=True)),
                ('dew_point', models.FloatField(null=True, blank=True)),
                ('humidity', models.FloatField(null=True, blank=True)),
                ('cloud_cover', models.FloatField(null=True, blank=True)),
                ('pressure', models.FloatField(null=True, blank=True)),
                ('wind_speed', models.FloatField(null=True, blank=True)),
                ('wind_bearing', models.FloatField(null=True, blank=True)),
                ('precip_intensity', models.FloatField(null=True, blank=True)),
                ('precip_probability', models.FloatField(null=True, blank=True)),
            ],
            options={
                'verbose_name': 'observation',
                'verbose_name_plural': 'observations',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Place',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('comments', models.TextField(null=True, blank=True)),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
            ],
            options={
                'verbose_name': 'place',
                'verbose_name_plural': 'places',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SquareArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('comments', models.TextField(null=True, blank=True)),
                ('longitude_min', models.FloatField()),
                ('longitude_max', models.FloatField()),
                ('latitude_min', models.FloatField()),
                ('latitude_max', models.FloatField()),
                ('n_points', models.SmallIntegerField()),
            ],
            options={
                'verbose_name': 'square area',
                'verbose_name_plural': 'square areas',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='observation',
            unique_together=set([('longitude', 'latitude', 'time', 'observed')]),
        ),
    ]
