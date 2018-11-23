from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from products.models import Product
import json


# Create your views here.
def add_to_cart(request):
    product_id = request.POST['product'] 
    quantity = int(request.POST['quantity'])
    
    cart = request.session.get('cart', {})
    cart[product_id] = cart.get(product_id, 0) + quantity
    request.session['cart'] = cart

    return redirect("/")
    

    
    
    
def view_cart(request):
    cart = request.session.get('cart', {})
    
    
    cart_items = []
    for product_id, quantity in cart.items(): #load each item through the id
        product = get_object_or_404(Product, pk=product_id) #load the product through the id
       
    
        cart_items.append({ #make a dictionary with the element you got through the id
            'id': product.id,
            'name': product.name,
            'brand': product.brand,
            'sku': product.sku,
            'description': product.description,
            'image': product.image,
            'price': product.price,
            'stock': product.stock,
            'quantity': quantity,
            'total': product.price * quantity,
        })    
        
    cart_total=0
    for item in cart_items:
        cart_total+=item['total']
    
    return render(request, "cart/view_cart.html", {'cart_items': cart_items, 'cart_total':cart_total})
    
    
def remove_from_cart(request):
    product_id = request.POST['product'] 
    
    
    cart = request.session.get('cart', {})
    del cart[product_id]
    request.session['cart']=cart
    
    

    return redirect("/cart/view_cart/")
    