# Generated by Django 4.2 on 2023-05-23 18:06

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_voting_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='voting',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 5, 23, 21, 6, 6, 32058, tzinfo=datetime.timezone.utc)),
        ),
    ]
