from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from reviews.forms import ReviewForm



# Create your views here.
def product_list(request):
    products = Product.objects.all()
    return render(request, "products/product_list.html", {'products': products})
    
#def product_details(request,id):
 #   products = Product.objects.get(pk=id)
 #   return render(request, "products/product_detail.html", {'products': products})
    
def product_details(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ReviewForm()
    return render(request, "products/product_detail.html", {"product" : product, "form": form})