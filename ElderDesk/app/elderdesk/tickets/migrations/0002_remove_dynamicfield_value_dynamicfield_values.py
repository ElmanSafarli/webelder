# Generated by Django 5.1 on 2024-09-13 10:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dynamicfield',
            name='value',
        ),
        migrations.AddField(
            model_name='dynamicfield',
            name='values',
            field=models.TextField(default=1, help_text='Comma-separated values'),
            preserve_default=False,
        ),
    ]
