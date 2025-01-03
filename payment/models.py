from django.db import models
from django.contrib.auth.models import User
from item.models import Cart, Item
 

class DeliveryAddress(models.Model):
    cart_id = models.CharField(max_length=55, blank=True, null=True)
    name = models.CharField(max_length=255, blank=True, null=True)
    division = models.CharField(max_length=255, blank=True, null=True)
    district = models.CharField(max_length=255, blank=True, null=True)
    upazila = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True) 
    contact_no = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.name}"
    
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField()
    status = models.CharField(max_length=50, default="Pending")  # e.g., Pending, Completed

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.FloatField()  # Store the item's price at the time of order

    def __str__(self):
        return f"#{self.order.id} - {self.order.user.username} - {self.quantity} x {self.item.name}"
    
 

 