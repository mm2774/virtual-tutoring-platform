# Generated by Django 3.1 on 2020-08-28 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meetings', '0004_auto_20200828_0409'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='meeting',
            name='status',
        ),
    ]