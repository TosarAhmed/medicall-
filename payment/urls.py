from django.urls import path
from . import views

app_name='payment'

urlpatterns = [
    path('delivery_address/<str:subtotal>/<str:cartid>/', views.delivery_address, name='delivery-address'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-confirmation/<int:order_id>/', views.order_confirmation, name='order_confirmation'),
]