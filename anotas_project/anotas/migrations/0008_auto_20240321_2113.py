# Generated by Django 2.2.28 on 2024-03-21 21:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('anotas', '0007_auto_20240321_2015'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='userID',
            new_name='user',
        ),
    ]