# Generated by Django 2.0.2 on 2018-04-02 22:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0015_partialsolution'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='partialsolution',
            name='language',
        ),
        migrations.RemoveField(
            model_name='partialsolution',
            name='modified',
        ),
        migrations.RemoveField(
            model_name='partialsolution',
            name='output',
        ),
        migrations.AlterField(
            model_name='partialsolution',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='partial_solutions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='partialsolution',
            name='problem',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='partial_solutions', to='restapi.Problem'),
        ),
    ]