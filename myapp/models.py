from django.db import models
import datetime

class Category(models.Model):
    category=models.CharField(max_length=50,blank=True,null=True)
    def __str__(self):
        return self.category

class Customer(models.Model):
    first_name=models.CharField(max_length=50,blank=True,null=True)
    last_name=models.CharField(max_length=50,blank=True,null=True)
    email=models.EmailField(max_length=50,blank=True,null=True)
    phone=models.IntegerField(blank=True,null=True)
    password=models.CharField(max_length=50,blank=True,null=True)
   
    def __str__(self):
        return f'{self.first_name}{self.last_name}'
    
class Product(models.Model):
    name=models.CharField(max_length=100,blank=True,null=True)
    price=models.DecimalField(blank=True,null=True,default=0,max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,default=1)
    description=models.CharField(max_length=2000,blank=True,null=True)
    image=models.ImageField(upload_to='uploads/products/')

    def __str__(self):
        return self.name
    
class Order(models.Model):
    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    customer=models.ForeignKey(Customer,on_delete=models.CASCADE)
    quantity=models.IntegerField(blank=True,null=True,default=1)
    address=models.CharField(max_length=300,blank=True,null=True)
    phone=models.CharField(max_length=20,blank=True,null=True)
    date=models.DateField(default=datetime.datetime.today)
    status=models.BooleanField(default=False)
    
    def __str__(self):
        return self.product

