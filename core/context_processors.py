from item.models import Cart

def cart_item_count(request):
    """
    A context processor to inject the count of cart items into all templates.
    """
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            count = sum(item.quantity for item in cart.cart_items.all())
        except Cart.DoesNotExist:
            count = 0
    else:
        # For unauthenticated users, use session-based cart if implemented
        cart = request.session.get('cart', {})
        count = sum(item['quantity'] for item in cart.values())

    return {'cart_item_count': count}