# Generated by Django 3.2.1 on 2024-05-16 16:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0003_alter_contact_contact_email_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='contact_subject',
            field=models.TextField(verbose_name='Subject'),
        ),
    ]
