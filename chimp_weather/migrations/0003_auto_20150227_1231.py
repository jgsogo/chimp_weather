# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chimp_weather', '0002_auto_20150227_1157'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='grid',
            name='n_vertices',
        ),
        migrations.RemoveField(
            model_name='grid',
            name='type',
        ),
        migrations.AddField(
            model_name='grid',
            name='_n_vertices',
            field=models.PositiveIntegerField(default=0, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='grid',
            name='_type',
            field=models.IntegerField(default=0, editable=False, choices=[(0, 'quad'), (1, 'triangles')]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='grid',
            name='_polygon',
            field=models.TextField(editable=False),
            preserve_default=True,
        ),
    ]
