# Generated by Django 4.2 on 2023-05-05 16:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='theme',
            old_name='userId',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='voteagainst',
            old_name='themeId',
            new_name='theme',
        ),
        migrations.RenameField(
            model_name='voteagainst',
            old_name='userId',
            new_name='user',
        ),
        migrations.RenameField(
            model_name='votefor',
            old_name='themeId',
            new_name='theme',
        ),
        migrations.RenameField(
            model_name='votefor',
            old_name='userId',
            new_name='user',
        ),
    ]