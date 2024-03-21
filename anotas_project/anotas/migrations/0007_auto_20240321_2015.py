# Generated by Django 2.2.28 on 2024-03-21 20:15

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('anotas', '0006_auto_20240312_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True)),
                ('views', models.IntegerField(default=0)),
                ('slug', models.SlugField(unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='page',
            name='category',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='user',
            new_name='userID',
        ),
        migrations.RemoveField(
            model_name='note',
            name='content',
        ),
        migrations.AddField(
            model_name='note',
            name='copyCount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='note',
            name='past_owners',
            field=models.CharField(blank=True, max_length=255),
        ),
        migrations.AddField(
            model_name='note',
            name='userID',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='anotas.UserProfile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='note',
            name='viewCount',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='note',
            name='lastSave',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='note',
            name='noteTitle',
            field=models.CharField(max_length=128, unique=True),
        ),
        migrations.AlterField(
            model_name='note',
            name='subject',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='anotas.Subject'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.DeleteModel(
            name='Page',
        ),
    ]
