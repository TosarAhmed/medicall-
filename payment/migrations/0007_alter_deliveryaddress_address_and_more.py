# Generated by Django 5.1.2 on 2025-01-03 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0006_remove_order_address_remove_order_contact_no_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deliveryaddress',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryaddress',
            name='contact_no',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryaddress',
            name='district',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryaddress',
            name='division',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryaddress',
            name='name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='deliveryaddress',
            name='upazila',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
