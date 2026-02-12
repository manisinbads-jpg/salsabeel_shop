from django.shortcuts import render
from products.models import Product, Category


def home(request):
    return render(request, 'core/home.html')
