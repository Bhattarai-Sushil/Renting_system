# Generated by Django 4.1 on 2023-12-01 01:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('houserent', '0013_booking_flat_remove_bookings_flat_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='flat',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='houserent.flatsavailable'),
        ),
    ]
