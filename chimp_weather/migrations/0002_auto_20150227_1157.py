# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chimp_weather', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grid',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('comments', models.TextField()),
                ('type', models.IntegerField(choices=[(0, 'quad'), (1, 'triangles')])),
                ('_polygon', models.TextField()),
                ('n_vertices', models.PositiveIntegerField()),
                ('timestamp', models.DateTimeField(auto_now=True, auto_now_add=True)),
            ],
            options={
                'verbose_name': 'grid',
                'verbose_name_plural': 'grids',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='observation',
            name='_non_forecast',
            field=models.BooleanField(default=None),
            preserve_default=True,
        ),
    ]
