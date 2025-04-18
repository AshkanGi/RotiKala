# Generated by Django 5.2 on 2025-04-08 10:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cart', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='first_name',
            new_name='full_name',
        ),
        migrations.RenameField(
            model_name='address',
            old_name='national_code',
            new_name='zip_code',
        ),
        migrations.RemoveField(
            model_name='address',
            name='last_name',
        ),
        migrations.RemoveField(
            model_name='address',
            name='license_plate',
        ),
        migrations.RemoveField(
            model_name='address',
            name='postal_code',
        ),
        migrations.RemoveField(
            model_name='address',
            name='unit',
        ),
    ]
