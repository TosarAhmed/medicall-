# Generated by Django 5.1.2 on 2025-01-03 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('item', '0006_remove_cart_items_alter_cart_user_cartitem'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='item',
            name='mg',
            field=models.TextField(blank=True, max_length=50, null=True, verbose_name='Unit'),
        ),
    ]