# Generated by Django 3.0.14 on 2022-09-24 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0010_auto_20220924_1945'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tweets',
            name='created_at_time',
        ),
    ]
