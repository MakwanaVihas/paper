# Generated by Django 3.0.6 on 2020-06-25 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_article_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='comm_count',
            field=models.IntegerField(default=0),
        ),
    ]
