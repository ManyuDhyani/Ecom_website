from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

class HomeView(View):
 def get(self, request):
  topwears = Product.objects.filter(category='TW')
  bottomwears = Product.objects.filter(category='BW')
  mobiles = Product.objects.filter(category='M')
  return render(request, 'app/home.html', {'topwears':topwears, 'bottomwears':bottomwears, 'mobiles':mobiles})

class product_detail(View):
 def get(self, request, pk):
  product = Product.objects.get(pk=pk)
  return render(request, 'app/productdetail.html', {'product': product})

def add_to_cart(request):
 user = request.user
 product_id = request.GET.get('prod_id')
 Cart.objects.get_or_create(user=user, product_id=int(product_id))
 return redirect('/cart')

@login_required(login_url='/account/login/')
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  carts=Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]

  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    total_amount = amount + shipping_amount
   return render(request, 'app/addtocart.html', {'carts': carts, 'total_amount': total_amount, 'amount': amount})
  else:
   return  render(request, 'app/emptycart.html')

def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity += 1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]

  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount

  data = {
   'quantity': c.quantity,
   'amount': amount,
   'total_amount': amount + shipping_amount,
  }
  return  JsonResponse(data)


def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity -= 1
  c.save()
  if c.quantity == 0:
   c.delete()
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]

  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount

  data = {
   'quantity': c.quantity,
   'amount': amount,
   'total_amount': amount + shipping_amount,
  }
  return  JsonResponse(data)

def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]

  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount

  data = {
   'amount': amount,
   'total_amount': amount + shipping_amount,
  }
  return  JsonResponse(data)


def countCartItem(request):
 cartItemCount = None
 if request.user.is_authenticated:
  cartItemCount = Cart.objects.filter(user=request.user).count()
 return {'cartItemCount': cartItemCount}

@login_required(login_url='/account/login/')
def checkout(request):
 user = request.user
 address = Customer.objects.filter(user=user)
 cart_items = Cart.objects.filter(user=user)

 amount = 0.0
 shipping_amount = 70.0
 total_amount = 0.0
 cart_product = [p for p in Cart.objects.all() if p.user == request.user]

 if cart_product:
  for p in cart_product:
   tempamount = (p.quantity * p.product.discounted_price)
   amount += tempamount
  total_amount = amount+shipping_amount

 return render(request, 'app/checkout.html', {'address': address, 'total_amount': total_amount, 'cart_items': cart_items})

@login_required(login_url='/account/login/')
def payment_done(request):
 user = request.user
 custid = request.GET.get('custid')
 customer = Customer.objects.get(id=custid)
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user, customer=customer, product=c.product, quantity=c.quantity).save()
  c.delete()
 return redirect("orders")
 
@login_required(login_url='/account/login/')
def address(request):
 address = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'address': address, 'active': 'btn-primary'})

@login_required(login_url='/account/login/')
def orders(request):
 orders_placed = OrderPlaced.objects.filter(user=request.user)
 return render(request, 'app/orders.html', {'orders_placed': orders_placed})

def buynow(request):
 return render(request, 'app/orders.html')

def change_password(request):
 return render(request, 'app/changepassword.html')

def mobile(request, data=None):
 if data:
  mobiles = Product.objects.filter(category='M').filter(brand=data)
 elif data == 'all':
  mobiles = Product.objects.filter(category='M')
 return render(request, 'app/mobile.html', {'mobiles': mobiles})

class CustomerRegistrationView(View):
 def get(self, request):
  form = CustomerRegistrationForm()
  return render(request, 'app/register.html', {'form': form})

 def post(self, request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratulations!! Resgistered Successfully.')
   form.save()
  return render(request, 'app/register.html', {'form': form})


class ProfileView(View):
 def get(self, request):
  form = CustomerProfileForm()
  return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})

 def post(self, request):
  form = CustomerProfileForm(request.POST)
  if form.is_valid():
   user = request.user
   name = form.cleaned_data['name']
   locality = form.cleaned_data['locality']
   city = form.cleaned_data['city']
   state = form.cleaned_data['state']
   zipcode = form.cleaned_data['zipcode']
   customerData = Customer(user=user, name=name, locality=locality, city=city, state=state, zipcode=zipcode)
   customerData.save()
   messages.success(request, 'Congratulations!! Profile Updated Successfully.')
  return render(request, 'app/profile.html', {'form': form, 'active': 'btn-primary'})