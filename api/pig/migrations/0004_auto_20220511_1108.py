# Generated by Django 3.1.5 on 2022-05-11 06:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pig', '0003_auto_20220510_1153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pig',
            old_name='weight_count',
            new_name='point_count',
        ),
    ]
