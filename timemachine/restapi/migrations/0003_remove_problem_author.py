# Generated by Django 2.0.2 on 2018-03-05 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0002_auto_20180305_1230'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='author',
        ),
    ]
