# Generated by Django 4.2.7 on 2024-03-19 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_userprofile_is_active'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='is_active',
        ),
    ]
