from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, render
from .models import Cart
from django.contrib import messages
from store.models import Product
from decimal import Decimal


class CartView(LoginRequiredMixin, View):
    template_name = 'cart.html'
    login_url = '/user/login/' 
    redirect_field_name = 'next'
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.info(request, "You need to be signed in to view your cart.")
        return super().dispatch(request, *args, **kwargs) 
    
    def get(self, request, error=None):
        """GET requests - render the cart with items and totals."""
        error = error
        total_weight = 0
        cart_items = []

        if request.user.is_authenticated:
            cart = get_object_or_404(Cart, user=request.user)
            cart_items = cart.items.select_related('product')
            total_weight = sum(item.pack_weight for item in cart_items)
        
        shipping_cost_per_kg = self.get_shipping_cost_per_kg(total_weight)
        subtotal = sum(item.calculate_total_price() for item in cart_items)
        shipping_cost = Decimal(total_weight) * Decimal(shipping_cost_per_kg)
        
        context = {
            'error': error,
            'current_page': 'Cart',
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
        print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print("action ",action)
        try:
            product_id = int(product_id)
            cart = get_object_or_404(Cart, user=request.user)
            
            if action == 'update':
                error = self.update_cart_item(request, cart, product_id)
                
            elif action == 'delete':
                self.delete_cart_item(cart, product_id)
        
        except (TypeError, ValueError):
            error = "Unexpected error occurred"
        
        return self.get(request, error)
    
    def update_cart_item(self, request, cart, product_id):
        """Updates weight of the product in the cart.
        The logic behind product being available is that if the weight 
        available is less than the minimum weight available, which is 
        the minimum weight of the product multiplied by 10, then the 
        product is not available.
        
        So, if the weight available is less than the new weight, then 
        the product is not available. If selected weight is more than 
        the available weight, then the error message is returned.
        
        If the product weight available minus the new weight is less
        than the minimum weight available, then the new weight is set
        to the weight available minus the minimum weight available and 
        next time the user tries to update the weight, user will be 
        notified that more weight is not available. (by error message).
        """
        new_weight = request.POST.get('new_weight')
        cart_item = cart.items.get(product_id=product_id)
        new_weight = float(new_weight) - float(cart_item.pack_weight)
        product = Product.objects.get(id=product_id)
        if Decimal(str(product.weight_available)) < Decimal(str(new_weight)):
            error = f"Selected Weight not available for {product}!"
            return error
        else:
            if product._is_available() or float(new_weight) < 0:
                if product.weight_available - new_weight < product._get_min_weight_available():
                    new_weight = product.weight_available - float(product._get_min_weight_available())
                product.weight_available = Decimal(str(product.weight_available)) - Decimal(str(new_weight))
                cart_item.pack_weight += Decimal(str(new_weight))
                product.save()
                cart_item.save()
            else:
                error = f"More weight not available for {product}!"
                return error
        return None
    
    def delete_cart_item(self, cart, product_id):
        cart_item = cart.items.get(product_id=product_id)
        product = cart_item.product
        product.weight_available += float(cart_item.pack_weight)
        product.save()
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
