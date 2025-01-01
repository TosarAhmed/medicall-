from django.urls import path, include 
from .views import detail, new, delete, edit, items, add_to_cart, cart_items

app_name='item'

urlpatterns = [
    path('', items, name='items'),
    path('new/', new, name = 'new'),
    path('<int:pk>', detail, name='detail'),
    path('<int:pk>/delete/', delete, name='delete'),
    path('<int:pk>/edit/', edit, name='edit'),
    path('add-to-cart/', add_to_cart, name='add_to_cart'),
    path('cart_items/', cart_items, name='cart-items'),
]

# http://127.0.0.1:8000/items/add-to-cart/?item_id=16

