# Generated by Django 4.1 on 2023-11-27 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('houserent', '0009_flatsavailable_uid'),
    ]

    operations = [
        migrations.RenameField(
            model_name='flatsavailable',
            old_name='price',
            new_name='required_price',
        ),
        migrations.AddField(
            model_name='flatsavailable',
            name='post_status',
            field=models.CharField(choices=[('r', 'requested'), ('a', 'approved'), ('s', 'successful'), ('x', 'rejected')], default='r', max_length=1),
        ),
        migrations.AddField(
            model_name='flatsavailable',
            name='recieved_price',
            field=models.IntegerField(default=0),
        ),
    ]
