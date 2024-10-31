def cart_items(request):
    items_in_cart = 0
    if request.user.is_authenticated:
        items_in_cart = request.user.cart.total_items_in_cart()
    return {'items_in_cart': items_in_cart}
