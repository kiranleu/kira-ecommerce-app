from django.shortcuts import render, redirect
from products.views import product_details
from .forms import ReviewForm
from products.models import Product

def write_review(request, id):
    form = ReviewForm(request.POST)
    review = form.save(commit=False)
    review.product_id = id
    review.author = request.user
    review.save()
    return redirect("product_detail", id=id)