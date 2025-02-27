# Generated by Django 5.1.2 on 2025-01-03 06:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0009_remove_cart_is_orderd'),
        ('payment', '0002_deliveryaddress_remove_deliverypayment_cart_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='delivery',
            name='address',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='payment',
        ),
        migrations.RemoveField(
            model_name='delivery',
            name='user',
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('division', models.CharField(max_length=255)),
                ('district', models.CharField(max_length=255)),
                ('upazila', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('contact_no', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('total_price', models.FloatField()),
                ('status', models.CharField(default='Pending', max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('price', models.FloatField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='item.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_items', to='payment.order')),
            ],
        ),
        migrations.DeleteModel(
            name='DeliveryAddress',
        ),
        migrations.DeleteModel(
            name='deliveryPayment',
        ),
        migrations.DeleteModel(
            name='Delivery',
        ),
    ]
