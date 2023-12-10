from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,null=True,blank=True,on_delete=models.CASCADE)
    name=models.CharField(max_length=250,null=True)
    email=models.CharField(max_length=200,null=True)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.FloatField()
    category=models.CharField(max_length=200,null=True)
    color=models.CharField(max_length=100,null=True)
    image=models.ImageField(null=True,blank=True)
    digital=models.BooleanField(default=False,null=True,blank=False) #whether the product is digitial product or not

    def __str__(self):
        return self.name
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url=''
        return url
    
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,null=True,blank=False)
    transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)
    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        return sum([item.getTotal for item in orderitems])
    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        return sum([item.quantity for item in orderitems])
    
    @property
    def shipping(self):
        shipping=False
        orderitems=self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital==False:
                shipping=True
        return shipping


class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)    
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True) 
    quantity=models.IntegerField(default=0,null=True,blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def getTotal(self):
        return self.quantity*self.product.price

class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,null=True,on_delete=models.SET_NULL)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
    