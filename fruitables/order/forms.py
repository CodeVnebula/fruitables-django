from decimal import Decimal
from django import forms
from .models import CartItem

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'pack_weight']

    def clean(self):
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
