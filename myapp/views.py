from django.shortcuts import render
from .models import Product
from random import shuffle
# Create your views here.
def login(request):
    return render(request,"login.html")
def home(request):
    products = list(Product.objects.all())

    # Shuffle the list of Product objects
    shuffle(products)

    return render(request,"home.html",{'products':products})
