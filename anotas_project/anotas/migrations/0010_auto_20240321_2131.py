# Generated by Django 2.2.28 on 2024-03-21 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('anotas', '0009_auto_20240321_2125'),
    ]

    operations = [
        migrations.AlterField(
            model_name='note',
            name='past_owners',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]