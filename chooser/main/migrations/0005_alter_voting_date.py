# Generated by Django 4.2 on 2023-05-24 11:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_alter_voting_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 24, 14, 52, 28, 135756, tzinfo=datetime.timezone.utc)),
        ),
    ]
