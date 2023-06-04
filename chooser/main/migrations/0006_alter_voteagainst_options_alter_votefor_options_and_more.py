# Generated by Django 4.2 on 2023-06-04 10:23

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0005_alter_voting_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='voteagainst',
            options={'verbose_name_plural': 'Votes against'},
        ),
        migrations.AlterModelOptions(
            name='votefor',
            options={'verbose_name_plural': 'Votes for'},
        ),
        migrations.AlterField(
            model_name='voting',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 6, 4, 13, 23, 56, 115644, tzinfo=datetime.timezone.utc)),
        ),
        migrations.CreateModel(
            name='Complaint',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('voting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.voting')),
            ],
        ),
    ]
