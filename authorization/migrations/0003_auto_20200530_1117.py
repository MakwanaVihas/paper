# Generated by Django 3.0.6 on 2020-05-30 11:17

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0002_auto_20200529_1327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='tags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=50), blank=True, null=True, size=None),
        ),
    ]
