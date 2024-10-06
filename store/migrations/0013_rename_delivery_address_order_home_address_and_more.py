# Generated by Django 5.1.1 on 2024-10-02 20:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_order_delivery_address_order_delivery_option'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='delivery_address',
            new_name='home_address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='delivery_option',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_method',
            field=models.CharField(blank=True, choices=[('parcel_machine', 'Parcel Machine'), ('post_office', 'Post Office'), ('courier', 'Courier'), ('pickup', 'Pick up by Yourself')], max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='parcel_machine_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='post_office_location',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
