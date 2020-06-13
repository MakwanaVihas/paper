# Generated by Django 3.0.6 on 2020-06-13 19:11

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authorization', '0004_user_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='user_preference',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
