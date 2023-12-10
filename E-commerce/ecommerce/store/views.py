import json
from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import *
import datetime
from django.views.decorators.csrf import csrf_exempt


def store(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		cartItems=order.get_cart_items
	else:
		order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
		items=[]
		cartItems=order["get_cart_items"]
	products=Product.objects.all()
	context = {'products':products,'cartItems':cartItems}
	return render(request, 'store/store.html', context)

@csrf_exempt
def cart(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		print(order.complete)
		items=order.orderitem_set.all()
		cartItems=order.get_cart_items
	else:
		items=[]
		cartItems=order["get_cart_items"]
		order={'get_cart_total':0,'get_cart_items':0,'shipping':False}

	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

@csrf_exempt
def checkout(request):
	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer,complete=False)
		items=order.orderitem_set.all()
		cartItems=order.get_cart_items
	else:
		order={'get_cart_total':0,'get_cart_items':0,'shipping':False}
		items=[]
		cartItems=order["get_cart_items"]
	context = {'items':items,'order':order,'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

@csrf_exempt
def updateItem(request):
	data=json.loads(request.body)
	productId=data['productId']
	action=data['action']
	print('Action:',action)
	print('Product:',productId)

	customer=request.user.customer
	product=Product.objects.get(id=productId)
	order,created=Order.objects.get_or_create(customer=customer,complete=False)

	orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

	if action=='add':
		orderItem.quantity=orderItem.quantity+1
	elif action=='remove':
		orderItem.quantity=orderItem.quantity-1
	orderItem.save()

	if orderItem.quantity<=0:
		orderItem.delete()
	return JsonResponse("Item was added",safe=False)



def processOrder(request):
	transaction_id=datetime.datetime.now().timestamp()
	data=json.loads(request.body)
	if request.user.is_authenticated:
		customer=request.user.customer
		order,created=Order.objects.get_or_create(customer=customer)
		total=float(data['form']['total'])
		order.transaction_id=transaction_id
		if total==order.get_cart_total:
			order.complete=True
		order.save()
		if order.shipping==True:
			ShippingAddress.objects.create(
				customer=customer,
				order=order,
				address=data['shipping']['address'],
				city=data['shipping']['state'],
				zipcode=data['shipping']['zipcode'],
			)
	else:
		print("user not logged in")
	
	return JsonResponse('Payement Submitted',safe=False)