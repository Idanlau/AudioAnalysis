# Generated by Django 3.2.5 on 2021-08-03 17:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Processing', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='audio',
            name='File',
        ),
        migrations.AddField(
            model_name='audio',
            name='accuracy',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='d_notes',
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name='audio',
            name='decibel_l',
            field=models.TextField(blank=True),
        ),
    ]