# Generated by Django 4.1.5 on 2023-04-22 14:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_blocked_user_is_verified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_verified',
        ),
    ]
