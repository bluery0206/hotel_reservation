# Generated by Django 5.2 on 2025-04-17 03:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_amenity_room_booking_roomimages'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RoomImages',
            new_name='RoomImage',
        ),
    ]
