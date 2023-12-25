"""
URL configuration for projectbuy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path
from myapp import views
from django.urls import include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
   
    
    path('',views.home,name="home"),
    path('aboutus/',views.about,name="aboutus"),
    path('login/',views.login1,name="login"),
    path('search/',views.search_page,name="search"),
    path('logout/',views.logout1,name="logout"),
    path('register/',views.register,name="register"),
    path('product/<int:pk>',views.product,name="product"),
    path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/',views.cart_summary,name="cart"),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buycart/',views.buynow,name="buynow"),
    path('order/',views.order,name="order"),
    path('buynow/<int:p_id>/',views.buynow1,name="buynow1"),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
