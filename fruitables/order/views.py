from django.shortcuts import get_object_or_404, render
from django.db.models import F
from .models import Cart
from store.models import Product
from decimal import Decimal

def cart_view(request):
    error = None
    if request.method == 'POST':
        action = request.POST.get('action')
        product_id = float(request.POST.get('product_id'))
        cart = get_object_or_404(Cart, user=request.user)
        
        if action == 'update':
            new_weight = request.POST.get('new_weight')
            cart_item = cart.items.get(product_id=product_id)
            new_weight = float(new_weight) - float(cart_item.pack_weight)
            product = Product.objects.get(id=product_id)
            if Decimal(str(product.weight_available)) < Decimal(str(new_weight)):
                error = "Weight not available"
            else:
                product.weight_available = Decimal(str(product.weight_available)) - Decimal(str(new_weight))
                cart_item.pack_weight += Decimal(str(new_weight))
                product.save()
                cart_item.save()
        
        elif action == 'delete':
            cart_item = cart.items.get(product_id=product_id)
            cart_item.delete()
    
    total_items = 0
    total_weight = 0
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)
        total_items = cart.total_items_in_cart()
        cart_items = cart.items.select_related('product')
        total_weight = sum([item.pack_weight for item in cart_items])
        
    if total_weight < 5:
        shipping_cost_per_kg = 2
    elif total_weight < 10:
        shipping_cost_per_kg = 1.5
    elif total_weight < 20:
        shipping_cost_per_kg = 1
    else:
        shipping_cost_per_kg = 0
        
    subtotal = sum([item.calculate_total_price() for item in cart_items])
    shipping_cost = total_weight * shipping_cost_per_kg
    
    context = {
        'error': error,
        'current_page': 'Cart',
        'items_in_cart': total_items,
        'cart_items': cart_items,
        'total_weight': total_weight,
        'subtotal': subtotal,
        'shipping_cost': shipping_cost,
        'total_cost': subtotal + shipping_cost
    }
    return render(request, 'cart.html', context)

def checkout_view(request):
    return render(request, 'checkout.html')
