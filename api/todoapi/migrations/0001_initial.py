# Generated by Django 3.1.5 on 2022-05-10 08:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ToDo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=256)),
                ('t1', models.TextField(max_length=256)),
                ('t2', models.TextField(max_length=256)),
                ('t3', models.TextField(max_length=256)),
                ('t4', models.TextField(max_length=256)),
                ('t1_done', models.BooleanField(default=False)),
                ('t2_done', models.BooleanField(default=False)),
                ('t3_done', models.BooleanField(default=False)),
                ('t4_done', models.BooleanField(default=False)),
                ('weight', models.IntegerField(default=1)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
