from django.shortcuts import render
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
 return render(request, 'app/addtocart.html')

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