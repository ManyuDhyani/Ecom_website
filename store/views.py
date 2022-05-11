from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from .models import *
from .forms import CustomerRegistrationForm, CustomerProfileForm
from django.contrib import messages

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
 Cart(user=user, product_id=int(product_id)).save()
 return redirect('/cart')

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
   total_amount = amount + shipping_amount

  data = {
   'quantity': c.quantity,
   'amount': amount,
   'total_amount': total_amount,
  }
  return  JsonResponse(data)

def buy_now(request):
 return render(request, 'app/buynow.html')

def address(request):
 address = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html', {'address': address, 'active': 'btn-primary'})

def orders(request):
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