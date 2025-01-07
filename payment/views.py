from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Cart, Order, OrderItem, DeliveryAddress

@login_required
def delivery_address(request, subtotal, cartid):

    if request.method == 'POST':
        name = request.POST.get('name')
        division = request.POST.get('division')
        district = request.POST.get('district')
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        cart = get_object_or_404(Cart, user=request.user)

        new_address = DeliveryAddress()
        new_address.name = name
        new_address.division = division
        new_address.district = district
        new_address.address = address
        new_address.contact_no = phone
        new_address.cart_id = cart.id
        new_address.save()

        return redirect('payment:place_order')

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
    total_price += 50 # Delivery Cost
    # Delivery Address
    deliver_address_model = DeliveryAddress.objects.filter(cart_id=cart.id).order_by('-id').first()
    # Create the Order
    order = Order.objects.create(user=request.user, total_price=total_price, delivery_address=deliver_address_model,)
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
    return redirect('payment:order_confirmation', order_id=order.id)

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'payment/order_confirmation.html', {'order': order})

@login_required
def track_order(request):
    orders = Order.objects.filter(user=request.user).all()

    return render(request, 'payment/track_order.html', {"orders": orders})