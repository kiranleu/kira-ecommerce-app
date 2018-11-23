from django.shortcuts import render,redirect,get_object_or_404, HttpResponse
from products.models import Product
from .forms import MakePaymentForm,OrderForm
from .models import OrderLineItem
from django.conf import settings
from django.contrib import messages
import stripe
# Create your views here.

stripe.api_key = settings.STRIPE_SECRET_KEY

def get_cart_item_and_total(cart):


   grd_total=0
   cart_items = []
   for product_id, quantity in cart.items():

       product = get_object_or_404(Product, pk=product_id)
       grd_total+=product.price * quantity
       # print(quantity)

       cart_items.append({
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
   return {'cart_items': cart_items,'grd_total':grd_total}


def checkout(request):
   cart = request.session.get('cart', {})
   cart_item_and_total=get_cart_item_and_total(cart)
   payment_form=MakePaymentForm()
   order_form = OrderForm()
   context={'payment_form':payment_form,'order_form':order_form, 'publishable':settings.STRIPE_PUBLISHABLE_KEY}
   context.update(cart_item_and_total)
   return render(request, "checkout/checkout.html",context)
   
def submit_payment(request): #To save the order into the DB

    cart = request.session.get('cart', {})
    cart_item_and_total=get_cart_item_and_total(cart)

    payment_form = MakePaymentForm(request.POST)
    order_form = OrderForm(request.POST)

    
    if order_form.is_valid() and payment_form.is_valid():
         #Saves the order to the DB
        order = order_form.save()
        cart = request.session.get('cart', {})
        for product_id, quantity in cart.items():
            line_item = OrderLineItem()
            line_item.product_id = product_id
            line_item.quantity = quantity
            line_item.order = order
            line_item.save()
        
        # Grab the money and run
        total = cart_item_and_total['grd_total'] #FOR STRIPE all amoun is in penneys
        stripe_token=payment_form.cleaned_data['stripe_id']#cleaned data is the cc number without dashes or spaces. Is the STIPE ID after validation.

        try:#we call this and pass:

            total_in_cent = int(total*100)#We multiply *100. We dont decimals to STRIPE
            customer = stripe.Charge.create( #we pass to the charge:
                amount=total_in_cent,
                currency="EUR",
                description="Dummy Transaction",#We could put costumer name or product.
                card=stripe_token,#We are passing the card=token. This is the STRIPE token that they sent up.
            )

        except stripe.error.CardError:
            print("Declined")
            messages.error(request, "Your card was declined!")

        if customer.paid:
            print("Paid")
            messages.error(request, "You have successfully paid")
       
        
        #Clear the cart
        del request.session['cart']
            
    return redirect("/")