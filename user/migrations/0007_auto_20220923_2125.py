# Generated by Django 3.0.14 on 2022-09-23 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_auto_20220923_2123'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweets',
            name='is_active',
        ),
        migrations.AddField(
            model_name='tweets',
            name='is_posted',
            field=models.BooleanField(default=False),
        ),
    ]
