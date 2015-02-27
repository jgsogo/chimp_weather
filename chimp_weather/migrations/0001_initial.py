# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('comments', models.TextField()),
                ('_type', models.IntegerField(editable=False, choices=[(0, 'quad'), (1, 'triangles')])),
                ('_polygon', models.TextField(editable=False)),
                ('_n_vertices', models.PositiveIntegerField(editable=False)),
                ('timestamp', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ],
            options={
                'verbose_name': 'grid',
                'verbose_name_plural': 'grids',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GridData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField(help_text='Time for the observation')),
                ('observed', models.DateTimeField(help_text='When the observation was taken (call to API)')),
                ('_non_forecast', models.BooleanField(default=None)),
                ('set', models.PositiveSmallIntegerField()),
                ('temperature', models.TextField()),
                ('grid', models.ForeignKey(to='chimp_weather.Grid')),
            ],
            options={
                'verbose_name': 'grid data',
                'verbose_name_plural': 'grid data',
            },
            bases=(models.Model,),
        ),
    ]
