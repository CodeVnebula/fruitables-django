from django.views import View
from django.shortcuts import get_object_or_404, render
from .models import Cart
from store.models import Product
from decimal import Decimal


class CartView(View):
    template_name = 'cart.html'
    
    def get(self, request):
        """GET requests - render the cart with items and totals."""
        error = None
        total_items = 0
        total_weight = 0
        cart_items = []

        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
            total_items = cart.total_items_in_cart()
            cart_items = cart.items.select_related('product')
            # CartItem has pack weight field, representing the weight of the product in the cart.
            total_weight = sum(item.pack_weight for item in cart_items)
        
        shipping_cost_per_kg = self.get_shipping_cost_per_kg(total_weight)
        # 'calculate_total_price()' is a method in CartItem model 
        # that returns the total price of the product in the cart.
        subtotal = sum(item.calculate_total_price() for item in cart_items)
        shipping_cost = total_weight * shipping_cost_per_kg
        
        context = {
            'error': error,
            'current_page': 'Cart',
            'items_in_cart': total_items,
            'cart_items': cart_items,
            'total_weight': total_weight,
            'subtotal': subtotal,
            'shipping_cost': shipping_cost,
            'total_cost': subtotal + shipping_cost,
        }
        
        return render(request, self.template_name, context)
    
    def post(self, request):
        """POST requests, update product weight and delete product from cart."""
        error = None
        action = request.POST.get('action')
        product_id = request.POST.get('product_id')
        
        try:
            product_id = int(product_id)
            cart = get_object_or_404(Cart, user=request.user)
            
            if action == 'update':
                error = self.update_cart_item(request, cart, product_id)
                
            elif action == 'delete':
                self.delete_cart_item(cart, product_id)
        
        except (TypeError, ValueError):
            error = "Unexpected error occurred"
        
        return self.get(request)
    
    def update_cart_item(self, request, cart, product_id):
        """Updates the weight of the product in the cart. When the check button is clicked."""
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
    
    def delete_cart_item(self, cart, product_id):
        cart_item = cart.items.get(product_id=product_id)
        cart_item.delete()
    
    def get_shipping_cost_per_kg(self, total_weight):
        """ Simulating shipping cost based on total weight of the cart. """
        if total_weight < 5:
            return 2
        elif total_weight < 10:
            return 1.5
        elif total_weight < 20:
            return 1
        else:
            return 0


def checkout_view(request):
    return render(request, 'checkout.html')
