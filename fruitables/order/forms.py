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

        cart_item = CartItem.objects.filter(cart=cart, product=product).first()
        
        if cart_item:
            cart_item.pack_weight += pack_weight
            product.weight_available -= float(pack_weight)
            cart_item.save()
            product.save()
            cleaned_data = {}
            
        return cleaned_data
