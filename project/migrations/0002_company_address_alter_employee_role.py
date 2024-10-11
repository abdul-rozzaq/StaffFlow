# Generated by Django 5.1.1 on 2024-09-21 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='address',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='employee',
            name='role',
            field=models.CharField(max_length=128),
        ),
    ]
