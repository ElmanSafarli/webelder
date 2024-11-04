# Generated by Django 5.1 on 2024-09-13 10:31

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('organizations', '0002_organization_created_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='DynamicField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('title', models.CharField(max_length=255)),
                ('initiator', models.EmailField(max_length=254)),
                ('body', models.TextField()),
                ('ticket_id', models.CharField(max_length=10, unique=True)),
                ('files', models.FileField(blank=True, null=True, upload_to='uploads/tickets/')),
                ('status', models.CharField(choices=[('new', 'New'), ('open', 'Open'), ('pending', 'Pending'), ('closed', 'Closed')], default='new', max_length=10)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('assignee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='assigned_tickets', to='organizations.userprofile')),
                ('subscribers', models.ManyToManyField(blank=True, related_name='subscribed_tickets', to='organizations.userprofile')),
            ],
            options={
                'verbose_name': 'Ticket',
                'verbose_name_plural': 'Tickets',
            },
        ),
    ]
