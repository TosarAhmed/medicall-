# Generated by Django 5.1.2 on 2025-01-03 06:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0008_cart_is_orderd'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cart',
            name='is_orderd',
        ),
    ]
