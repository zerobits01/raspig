# Generated by Django 3.1.3 on 2020-12-06 09:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0002_delete_adminloginlock'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Token',
        ),
    ]
