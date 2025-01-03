from django.contrib.auth.decorators import login_required
from django.db.models import Q 
from django.shortcuts import render, get_object_or_404, redirect 
from .models import Category
from .models import Item, Cart, CartItem
from django.http import JsonResponse
from .forms import NewItemForm, EditItemForm
from django.shortcuts import get_object_or_404, redirect
from django.core.serializers import serialize

def safe_parse_int(value, base=10):
    try:
        return int(value, base)
    except ValueError:
        return None

def items(request):
    query = request.GET.get('query', '')
    search_category = request.GET.get('category', '')
    categories = Category.objects.all().order_by('order')
    items = Item.objects.filter(is_sold=False)
 
    current_category = ""
    if search_category:
        current_category = Category.objects.get(id=search_category).name
    if search_category:
        items = items.filter(category_id=search_category)
    if query:
        items = items.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'item/items.html', {
        'items': items,
        'query': query,
        'categories': categories,
        'search_category': safe_parse_int(search_category),
        'current_category': current_category,
    })

def detail(request, pk):
    item = get_object_or_404(Item, pk=pk)

    return render(request, 'item/detail.html', {
        'item': item,
    })

def add_to_cart(request):
    item_id = request.GET.get('item_id')
    quantity = int(request.GET.get('quantity', 1))  # Default to 1 if quantity is not provided

    if not item_id:
        return JsonResponse({'error': 'Item ID is required'}, status=400)

    # Retrieve the item object
    item = get_object_or_404(Item, id=item_id)

    # Simulate a user cart; in a real scenario, this could be linked to the logged-in user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if the item is already in the cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, item=item)

    if not created:
        # If the item is already in the cart, update the quantity
        cart_item.quantity += quantity
        cart_item.save()
        return JsonResponse({'message': f'Updated quantity for {item.name} to {cart_item.quantity}'}, status=200)
    else:
        # If the item is not in the cart, set the initial quantity
        cart_item.quantity = quantity
        cart_item.save()
        return JsonResponse({'message': f'Added {item.name} to cart with quantity {quantity}'}, status=200)

@login_required
def new(request):
    if request.method == 'POST':
        form = NewItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()

            return redirect ('item:detail', pk=item.id)
    else:
        form = NewItemForm()

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'New item',
    })

@login_required
def edit(request, pk):
    item = get_object_or_404(Item, pk=pk, created_by=request.user)
    if request.method == 'POST':
        form = EditItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()

            return redirect ('item:detail', pk=item.id)
    else:
        form = EditItemForm(instance=item)

    return render(request, 'item/form.html', {
        'form': form,
        'title': 'Edit item',
    })

@login_required
def delete(request, pk):
    item.delete()

    return redirect('dashboard:index')


@login_required
def delete_cart_item(request, itemid):

    
    # cart = Cart.objects.get(user=request.user)
    
    cart_item = CartItem.objects.get(id=itemid)
    # Delete the CartItem
    cart_item.delete()

    # print(cart_item)
    return redirect('item:cart-items')
    # else:
    #     return redirect('/')


@login_required
def cart_items(request):
    
    cart = Cart.objects.get(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    cart_total = sum(cart_item.item.price * cart_item.quantity for cart_item in cart.cart_items.all())

    for cart in cart_items:
        cart.total_price = cart.item.price * cart.quantity

    return render(request, 'item/cart_items.html', {'cart_items': cart_items, 'cart_total': cart_total, 'cart_id': cart.id})