from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponseNotFound,HttpResponseServerError,Http404
from django.db.models import F, Sum, DecimalField
from .models import Product
from random import shuffle
from .models import Order
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django import forms
from .models import Cart
from .models import CartItem
from .models import Category
from .forms import SignUpForm
from django.db.models import Q
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
# Create your views here.
def login1(request):
    if request.method=='POST':
        loginname=request.POST.get('loginname')
        loginpassword=request.POST.get('loginpassword')
        user=authenticate(request,username=loginname,password=loginpassword)
        print(user)
        print(loginname)
        print(loginpassword)
        if user is not None:
            login(request,user)
            messages.success(request,("You Have Been Logged In Successfully!!!"))
            return redirect('home')
        else:
            messages.success(request,("There Is An Error, Please Try Again!!!"))
            return redirect('login')

    
    else:
        return render(request,"login.html")
def home(request):
    products = list(Product.objects.all())

    # Shuffle the list of Product objects
    shuffle(products)

    return render(request,"home.html",{'products':products})

def about(request):
    return render(request,"aboutus.html")
def logout1(request):
    logout(request)
    messages.success(request,("You Have Been Logged Out Successfully!!!"))
    return redirect('home')

def register(request):
    form=SignUpForm()
    if request.method=="POST":
        form=SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username=form.cleaned_data['username']
            password=form.cleaned_data['password1']
            user=authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You Have Been Registered Successfully!!!"))
            return redirect('home')
        else:
            messages.success(request,("Oops! There Was A Problem In Registering, Please Try Again."))
            return redirect('register')

    else:
        return render(request,"register.html",{'form':form})
    
def product(request,pk):
    product=Product.objects.get(id=pk)
    similar=product.category
    similar_product=list(Product.objects.filter(category=similar))
    shuffle(similar_product)
    return render(request,"product.html",{'product':product,'similar':similar_product})
def search_page(request):
    if request.method=="POST":
        searchbar=request.POST['search']
        print(searchbar)
        if searchbar:
            
                split_word=searchbar.split()
                
                q_object=Q()
                

                for word in split_word:
                    q_object |=Q(name__icontains=word) 
                
                # Perform a query to find titles containing any of the specified words
                
                product=Product.objects.filter(q_object)
                return render(request,"search.html",{'product':product})
            
        else:
           return redirect('home')

        
    return render(request,"search.html",{'product':product})
def add_to_cart(request, item_id):
    item = get_object_or_404(Product, pk=item_id)
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, item=item)
        if not item_created:
            cart_item.quantity += 1
            cart_item.save()
    else:
        # For guest users, manage cart items using session
        if 'cart' not in request.session:
            request.session['cart'] = {}
        cart = request.session['cart']
        cart_item = cart.get(str(item_id))
        if cart_item:
            cart_item['quantity'] += 1
        else:
            cart[str(item_id)] = {'quantity': 1}
        request.session.modified = True
    
    return redirect('cart')  
def cart_summary(request):
    cart_items = CartItem.objects.filter(cart__user=request.user)  # Query cart items for the current user
    return render(request, 'cart_summary.html', {'cart_items': cart_items})
def remove_from_cart(request, cart_item_id):
    print(cart_item_id)
    try:
        Item=Product.objects.get(pk=cart_item_id)
        print(Item)
        cart_item = CartItem.objects.get(item=Item)
        cart_item.delete()  # Print the retrieved cart_item details
        
    except CartItem.DoesNotExist:
        print("CartItem with this ID does not exist")

    return redirect('cart')
def buynow(request):
    if request.method == 'POST':
        for cart_item in request.POST:
            if cart_item.startswith('qtycart_'):
                item_id = cart_item.split('_')[1]
                quantity = request.POST[cart_item]
                
                # Get the CartItem instance and update the quantity
                try:
                    cart_item_instance = CartItem.objects.get(item_id=item_id)
                    cart_item_instance.quantity = int(quantity)
                    cart_item_instance.save()
                except CartItem.DoesNotExist:
                    pass  # Handle if the item doesn't exist in the cart
                
        return redirect('buynow')  # Redirect to the same page after updating quantities

    # Retrieve cart items after updating quantities
    if request.user.is_authenticated:
        cart_items = CartItem.objects.filter(cart__user=request.user)
    else:
        # For guest users, handle cart items using session
        cart_items = []  # Replace this with your logic for guest users

    # Calculate total price
    total_price = cart_items.aggregate(total=Sum(F('quantity') * F('item__price'), output_field=DecimalField()))['total'] or 0  # If there are no items, set total_price to 0 # If there are no items, set total_price to 0

    return render(request, 'buynow.html', {'cart_items': cart_items, 'total_price': total_price})
    
def buynow1(request, p_id):
    product = get_object_or_404(Product, pk=p_id)
    total = 0
    qty = 0

    if request.method == "POST":
        print("HELLO")
        qty = request.POST.get('quantity')
        print(qty)  # Default value set to 0 if quantity is not provided
        price = int(product.price)
        total = price * int(qty)

    return render(request, "buynow1.html", {'i': product, 'total': total, 'qty': qty})
def order(request):
    if request.method == 'POST':
        # Extract address and phone from the form data
        address = request.POST.get('address')
        phone = request.POST.get('phone')

        # Check if address and phone are not empty
        if address and phone:
            # Process the cart items and create orders
            for cart_item in request.POST:
                if cart_item.startswith('qtycart_'):
                    item_id = cart_item.split('_')[1]
                    quantity = request.POST[cart_item]
                    
                    try:
                        cart_item_instance = CartItem.objects.get(item_id=item_id)
                        cart_item_instance.quantity = int(quantity)
                        cart_item_instance.save()
                    except CartItem.DoesNotExist:
                        pass  # Handle if the item doesn't exist in the cart
                    
            # Create Order instances from the cart items
            if request.user.is_authenticated:
                user_instance = User.objects.get(pk=request.user.pk)
                customer_instance = user_instance.first_name  # Access the related Customer instance
                
                cart_items = CartItem.objects.filter(cart__user=request.user)
                for cart_item in cart_items:
                    Order.objects.create(
                        product=cart_item.item,
                        customer=customer_instance,  # Assign the related Customer instance
                        quantity=cart_item.quantity,
                        address=address,
                        phone=phone,
                    )

            # Clear the user's cart after creating orders
            CartItem.objects.filter(cart__user=request.user).delete()

            return redirect('buynow')  # Redirect to the same page after creating orders and clearing the cart
        else:
            # Handle missing address or phone, maybe return an error or redirect to a page to fill in the details
            return redirect('address_form_page')  # Redirect to a page to fill in the missing details

    # Handle other HTTP methods or render a page for GET requests if needed
    return render(request, 'order.html')