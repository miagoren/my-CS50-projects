# Generated by Django 3.1.2 on 2020-11-10 10:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebAid', '0003_auto_20201110_1219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='opportunity',
            name='resolved',
            field=models.ForeignKey(blank=True, null=True, on_delete=models.SET(True), related_name='resolved', to=settings.AUTH_USER_MODEL),
        ),
    ]
