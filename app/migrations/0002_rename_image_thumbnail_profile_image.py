# Generated by Django 5.2 on 2025-04-15 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='image_thumbnail',
            new_name='image',
        ),
    ]
