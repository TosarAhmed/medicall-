from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem

@login_required
def delivery_address(request, subtotal, cartid):

    delivery_cost = 50
    total_amount = float(subtotal) + delivery_cost
    context = {
        'subtotal': subtotal,
        'cartid': cartid,
        'delivery_cost': delivery_cost,
        'total_amount': total_amount
    }

    return render(request, 'payment/confirm_delivery_address.html', context)


@login_required
def place_order(request):
    # Get the current user's cart
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cart_items.all()

    if not cart_items:
        return redirect('cart_view')  # Redirect to cart page if it's empty

    # Calculate total price
    total_price = sum(item.item.price * item.quantity for item in cart_items)

    # Create the Order
    order = Order.objects.create(user=request.user, total_price=total_price)

    # Create OrderItems for each CartItem
    for cart_item in cart_items:
        OrderItem.objects.create(
            order=order,
            item=cart_item.item,
            quantity=cart_item.quantity,
            price=cart_item.item.price,
        )

    # Clear the cart after placing the order
    cart.cart_items.all().delete()

    # Redirect to an order confirmation page
    return redirect('order_confirmation', order_id=order.id)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'order_confirmation.html', {'order': order})