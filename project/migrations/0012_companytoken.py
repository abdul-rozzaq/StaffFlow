# Generated by Django 5.1.3 on 2025-01-12 09:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0011_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(max_length=40, unique=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('company', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='auth_token', to='project.company')),
            ],
        ),
    ]
