from django.contrib import admin
from payment.models import Order, OrderItem, DeliveryAddress
# Register your models here.
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryAddress)