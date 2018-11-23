
def items_in_cart(request):
    cart = request.session.get('cart',{})
    count = 0
    for quantity in cart.values():
        count += quantity
        
    return {'items_in_cart':count}