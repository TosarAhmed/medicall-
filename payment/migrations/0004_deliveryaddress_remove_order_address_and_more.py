# Generated by Django 5.1.2 on 2025-01-03 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payment', '0003_remove_delivery_address_remove_delivery_cart_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_id', models.CharField(blank=True, max_length=55, null=True)),
                ('name', models.CharField(max_length=255)),
                ('division', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('upazila', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('contact_no', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='order',
            name='address',
        ),
        migrations.RemoveField(
            model_name='order',
            name='contact_no',
        ),
        migrations.RemoveField(
            model_name='order',
            name='district',
        ),
        migrations.RemoveField(
            model_name='order',
            name='division',
        ),
        migrations.RemoveField(
            model_name='order',
            name='name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='upazila',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payment.deliveryaddress'),
        ),
    ]
