# Generated by Django 3.1.2 on 2020-11-18 11:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('WebAid', '0011_auto_20201118_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='notifications',
        ),
    ]