from django.shortcuts import get_object_or_404, redirect, render
from store.models import Product
from store.views import cart_view
from .models import Cart


def cart(request):
    if request.user.is_authenticated:
        cart = get_object_or_404(Cart, user=request.user)

        cart_items = cart.items.select_related('product')
        products = []
        total_weight = 0
        for item in cart_items:
            product = item.product
            weight = product.pack_weight
            total_weight += weight
            products.append({
                'id': product.id,
                'name': product.name,
                'image': product.image.url,
                'pack_weight': weight,
                'min_weight': product.min_weight,
                'price': product.price,
                'total_price': product.calculate_price(),
            })

        if total_weight < 5:
            shipping_cost_per_kg = 2
        elif total_weight < 10:
            shipping_cost_per_kg = 1.5
        elif total_weight < 20:
            shipping_cost_per_kg = 1
        else:
            shipping_cost_per_kg = 0
            
        subtotal = sum([product['total_price'] for product in products])
        shipping_cost = total_weight * shipping_cost_per_kg 
            
        context = {
            'cart':cart_items,
            'products': products,
            'items_in_cart': len(products),
            'total_weight': total_weight,
            'subtotal': subtotal,
            'shipping': shipping_cost,
            'total': subtotal + shipping_cost,
        }
        return render(request, 'cart.html', context)
    else:
        context = {
            'products': [],
        }
        return render(request, 'cart.html', context)



def checkout(request):
    items_in_cart = cart_view(request)[0]
    context = {
        'items_in_cart': items_in_cart
    }
    return render(request, 'checkout.html', context)

def apply_weight(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        new_weight = float(request.POST.get('pack_weight'))  
        print(new_weight)
        product.pack_weight = new_weight
        product.save()
        return redirect('cart')  

def delete_item(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, id=product_id)
        product.delete()
        return redirect('cart')
    
