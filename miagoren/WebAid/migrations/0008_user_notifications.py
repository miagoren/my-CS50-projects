# Generated by Django 3.1.2 on 2020-11-16 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WebAid', '0007_conversation_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='notifications',
            field=models.TextField(blank=True, null=True),
        ),
    ]
