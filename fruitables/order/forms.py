from decimal import Decimal
from django import forms
from .models import CartItem

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'pack_weight']

    def clean(self):
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
        cleaned_data = super().clean()
        cart = cleaned_data.get('cart')
        product = cleaned_data.get('product')
        pack_weight = cleaned_data.get('pack_weight')
        
        if not cart or not product or pack_weight is None:
            raise forms.ValidationError("Cart, product, and pack weight must be provided.")
        
        if not product._is_available():
            raise forms.ValidationError(f"Not enough product weight available")

        min_weight_available = product._get_min_weight_available()

        if product.weight_available < min_weight_available:
            raise forms.ValidationError(f"Product is not available")

        if product.weight_available < pack_weight:
            raise forms.ValidationError(f"Selected weight is more than available weight")
        
        if product.weight_available - float(pack_weight) < float(product.min_weight):
            pack_weight = Decimal(product.weight_available) - float(product.min_weight)
            
        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        
        if cart_item:
            cart_item.pack_weight += pack_weight
            cart_item.save()
            cleaned_data = {}
        
        product.weight_available -= float(pack_weight)
        product.save()
        return cleaned_data
