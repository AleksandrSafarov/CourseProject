# Generated by Django 4.2 on 2023-05-22 13:44

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_theme_date_alter_theme_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='theme',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 22, 16, 44, 5, 485927, tzinfo=datetime.timezone.utc)),
        ),
    ]