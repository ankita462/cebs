from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.urls import *
from .models import Account,Product
from django.contrib import messages
from django.shortcuts import (get_object_or_404,render,HttpResponseRedirect)
from django.views import View
from django.contrib.auth.decorators import login_required
from .forms import *
from django.conf import settings
from django.urls import reverse
from django.contrib import messages
import stripe

# Create your views here.
def main(request):
    return render(request,'tryapp/user/frontpage.html')

def signup(request):
    context={}
    if request.user.is_authenticated:
        return redirect('home/')
    else:
        if request.method=='POST':
            if request.POST.get('username') and request.POST.get('email') and request.POST.get('password1'):
                form=RegistrationForm(request.POST)
                if form.is_valid():
                    form.save()
                    email=form.cleaned_data.get('email')
                    raw_password=form.cleaned_data.get('password1')
                    account=authenticate(email=email,password=raw_password)
                    login(request,account)
                    # messages.success(request,'Account was created for '+username)
                    return redirect('login/')
                else:
                    context['registration_form']=form
        else:
            form=RegistrationForm()
            context['registration_form']=form
        return render(request,'tryapp/user/signup.html',context)

def logout_view(request):
    logout(request)
    return redirect('main/')

def loginview(request,*args,**kwargs):
    context={}
    user=request.user
    print(user)
    if user.is_authenticated:
        return redirect('home/')

    if request.POST:
        form=AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email=request.POST['email']
            password=request.POST['password']
            is_superuser=request.POST.get('is_superuser')
            print(email," ",password," ",is_superuser)
            user=authenticate(email=email,password=password,is_superuser=is_superuser)
            
            if user:
                if user.is_superuser==True:
                    login(request,user)
                    return redirect('viewproduct/')
                else:
                   login(request,user)
                   return redirect('home/')
        else:
            messages.info(request,'Username or password is incorrect')
    else:
        form=AccountAuthenticationForm()
    context['login_form']=form
    return render(request,'tryapp/user/login.html',context)

@login_required(login_url='login')
def orderhistory(request):
    orderss=Order.objects.all()
    return render(request,'tryapp/user/orderhistory.html',{'orderss':orderss})

@login_required(login_url='login')
def addproductform(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('viewproduct/')
    else:
        form=ProductForm()
        context={'form':form}
        return render(request,'tryapp/admin/productadd.html',context)

@login_required(login_url='login')
def viewproduct(request):
    productss=Product.objects.all()
    return render(request,'tryapp/admin/viewproduct.html',{'productss':productss})

@login_required(login_url='login')
def vieworder(request):
    orderss=Order.objects.all()
    return render(request,'tryapp/admin/vieworder.html',{'orderss':orderss})
    
@login_required(login_url='login')
def updateproduct(request, id):
    obj = get_object_or_404(Product, id = id)
    form = ProductForm(request.POST or None, instance = obj)
    if form.is_valid():
        form.save()
        productss=Product.objects.all()
        return render(request,'tryapp/admin/viewproduct.html',{'productss':productss})
    context={'form':form}
    return render(request, "tryapp/admin/updateproduct.html", context)

@login_required(login_url='login')
def adminprofile(request):
    return render(request, 'tryapp/admin/adminprofile.html')

@login_required(login_url='login')
def deleteproduct(request, id):
    context ={}
    obj = get_object_or_404(Product, id = id)
    if request.method =="POST":
        obj.delete()
        productss=Product.objects.all()
        return render(request,'tryapp/admin/viewproduct.html',{'productss':productss})
  
    return render(request, "tryapp/admin/deleteproduct.html", context)

@login_required(login_url='login')
def updateprofile_view(request):
    if not request.user.is_authenticated:
        return redirect("login/")
    context={}

    if request.POST:
        form=UpdateProfileForm(request.POST,instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'Profile is updated successfully!')
    else:
        form=UpdateProfileForm(
            initial={
                "email": request.user.email,
                "username": request.user.username,
                "phone_no": request.user.phone_no,
            }
        )
    context['account_form']=form
    return render(request,'tryapp/user/profile.html',context)
    
def products(request):
    productss=Product.objects.all()
    return render(request,'tryapp/user/homepage.html',{'productss':productss})

def clothes(request):
    productss=Product.objects.filter(category='CLOTHES')
    return render(request,'tryapp/user/homepage.html',{'productss':productss})

def electronics(request):
    productss=Product.objects.filter(category='ELECTRONICS')
    return render(request,'tryapp/user/homepage.html',{'productss':productss})

def books(request):
    productss=Product.objects.filter(category='BOOKS')
    return render(request,'tryapp/user/homepage.html',{'productss':productss})

def shoes(request):
    productss=Product.objects.filter(category='SHOES')
    return render(request,'tryapp/user/homepage.html',{'productss':productss})

@login_required(login_url='login')
def viewdesc(request,id):
    product=Product.objects.get(pk=id)
    return render(request,'tryapp/user/view.html',{'product':product})

@login_required(login_url='login')
def contact(request):
    return render(request, 'tryapp/user/contact.html')

@login_required(login_url='login')
def viewuser(request):
    userss = Account.objects.all()
    return render(request, 'tryapp/admin/viewuser.html', {'userss': userss})



def vclothes(request):
    productss = Product.objects.filter(category='CLOTHES')
    return render(request, 'tryapp/admin/viewproduct.html', {'productss': productss})


def velectronics(request):
    productss = Product.objects.filter(category='ELECTRONICS')
    return render(request, 'tryapp/admin/viewproduct.html', {'productss': productss})


def vbooks(request):
    productss = Product.objects.filter(category='BOOKS')
    return render(request, 'tryapp/admin/viewproduct.html', {'productss': productss})


def vshoes(request):
    productss = Product.objects.filter(category='SHOES')
    return render(request, 'tryapp/admin/viewproduct.html', {'productss': productss})

def shipping(request,id):
    context = {}
    if request.method == 'POST':
        if request.POST.get('address') and request.POST.get('phone') and request.POST.get('quantity'):
            form = orderForm(request.POST)
            if form.is_valid():
                order=Order()
                product1=Product.objects.get(id=id)
                print(product1)
                quan=form.cleaned_data['quantity']
                print(quan)
                pri=product1.price*quan
                stripe.api_key = settings.STRIPE_PRIVATE_KEY
                print(settings.STRIPE_PRIVATE_KEY)
                # stripe_token = form.cleaned_data['stripe_token']
                try:
                    print('hello')
                    charge = stripe.Charge.create(
                    amount=int(pri)* 100,
                    currency='INR',
                    description='Cebs Product',
                    source='tok_visa'
                    )
                    order=Order()
                    product1=Product.objects.get(id=id)
                    order.productname=product1.productname
                    order.phone=form.cleaned_data['phone']
                    order.address=form.cleaned_data['address']
                    order.quantity=quan
                    order.username=Account.objects.get(id=request.user.id).username
                    order.price=product1.price
                    order.total=pri
                    order.save()
                    print(order)
                    return redirect('home')
                except Exception:
                    messages.error(request, 'There was something wrong with the payment')
                
            else:
                context['order_form'] = form
    else:
        form = orderForm()
    return render(request, 'tryapp/user/shipping.html', {'order_form': form, 'stripe_pub_key': settings.STRIPE_PUBLIC_KEY})

@login_required(login_url='login')
def usercart(request):
    return render(request, 'tryapp/user/usercart.html')





























# @login_required(login_url='login')
# def usercart(request):
#     return render(request,'tryapp/usercart.html')


# from apps.order.utilities import checkout, notify_customer, notify_vendor

# def usercart(request):
#     cart = Cart(request)

#     if request.method == 'POST':
#         form = CheckoutForm(request.POST)

#         if form.is_valid():
#             stripe.api_key = settings.STRIPE_SECRET_KEY

#             stripe_token = form.cleaned_data['stripe_token']

#             try:
#                 charge = stripe.Charge.create(
#                     amount=int(cart.get_total_cost() * 100),
#                     currency='USD',
#                     description='Charge from Interiorshop',
#                     source=stripe_token
#                 )

#                 # first_name = form.cleaned_data['first_name']
#                 # last_name = form.cleaned_data['last_name']
#                 email = form.cleaned_data['email']
#                 phone = form.cleaned_data['phone']
#                 address = form.cleaned_data['address']
#                 zipcode = form.cleaned_data['zipcode']
#                 place = form.cleaned_data['place']

#                 # order = checkout(request, email, address, zipcode, place, phone, cart.get_total_cost())

#                 cart.clear()

#                 # notify_customer(order)
#                 # notify_vendor(order)

#                 return redirect('success')
#             except Exception:
#                 messages.error(request, 'There was something wrong with the payment')
#     else:
#         form = CheckoutForm()

#     remove_from_cart = request.GET.get('remove_from_cart', '')
#     change_quantity = request.GET.get('change_quantity', '')
#     quantity = request.GET.get('quantity', 0)

#     if remove_from_cart:
#         cart.remove(remove_from_cart)

#         return redirect('cart')
    
#     if change_quantity:
#         cart.add(change_quantity, quantity, True)

#         return redirect('cart')

#     return render(request, 'tryapp/usercart.html', {'form': form, 'stripe_pub_key': settings.STRIPE_PUB_KEY})

# def success(request):
#     return render(request, 'cart/success.html')

# stripe.api_key = settings.STRIPE_PRIVATE_KEY


# class CreateCheckoutSessionView(View):
#     def post(self, request, *args, **kwargs):
#         product_id = self.kwargs["id"]
#         print(request.POST.get('address'))
#         product = Product.objects.get(id=product_id)
#         YOUR_DOMAIN = "http://127.0.0.1:8000"
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_types=['card'],
#             line_items=[
#                 {
#                     'price_data': {
#                         'currency': 'INR',
#                         'unit_amount': int(product.price)*100,
#                         'product_data': {
#                             'name': 'Cebs Product'
#                         },
#                     },
#                     'quantity': 1,
#                 },
#             ],
#             metadata={
#                 "product_id": product.id
#             },
#             mode='payment',
#             success_url=YOUR_DOMAIN + '/tryapp/orderh/',
#             cancel_url=YOUR_DOMAIN + '/tryapp/home/',
#         )
#         return JsonResponse({
#             'id': checkout_session.id
#         })


# def shipping(request,id):
#     context = {}
#     if request.method == 'POST':
#         if request.POST.get('address') and request.POST.get('phone') and request.POST.get('quantity'):
#             form = orderForm(request.POST)
#             if form.is_valid():
#                 order=Order()
#                 product1=Product.objects.get(id=id)
#                 order.product=product1
#                 order.phone=form.cleaned_data['phone']
#                 order.address=form.cleaned_data['address']
#                 order.quantity=form.cleaned_data['quantity']
#                 order.username=Account.objects.get(id=request.user.id).username
#                 order.price=product1.price
#                 order.save()
#                 return redirect('home/')
#                 # print()
#                 # context.update({
#                 #         "product": product1,
#                 #         "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLIC_KEY
#                 #     })
#                 # return context
#             else:
#                 context['order_form'] = form
#     else:
#         form = orderForm()
#         context['order_form']=form
#         return render(request, 'tryapp/shipping.html', context)
