from django.shortcuts import render,HttpResponseRedirect
from django.views import View
from .models import Customer,Product,Cart,OrderPlaced,Trending,DealOfDay
from .forms import CustomerRegistrationForm,LoginForm,PasswordChange,PasswordReset,SetPassword,CustomerProfileForm
from django.contrib.auth import login,authenticate,logout,update_session_auth_hash
from django.contrib import messages
from django.db.models import Q
from django.http import JsonResponse


class ProductView(View):
 def get(self,request):
  topwears=Product.objects.filter(category='TW')
  bottomwears=Product.objects.filter(category='BW')
  mobiles=Product.objects.filter(category='M')
  laptops=Product.objects.filter(category='L')
  trend=Trending.objects.filter()
  dday=DealOfDay.objects.filter()
  return render(request,'app/home.html',{'topwears':topwears,
        'bottomwears':bottomwears,'mobiles':mobiles,'laptops':laptops,
        'trend':trend,'dday':dday})


class ProductDetailView(View):
 def get(self,request,pk):
  product=Product.objects.get(pk=pk)
  item_already_in_cart = False
  if request.user.is_authenticated:
    item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
  return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})
 
def mobile(request,data=None):
  brands=['MOTOROLA','Samsung','APPLE','realme','Google','OnePlus']
  for b in brands:
    if data==None:
      mobiles=Product.objects.filter(category='M')
    elif data==b:
      mobiles=Product.objects.filter(category='M').filter(brand=data)
  if data=='below':
    mobiles=Product.objects.filter(category='M').filter(discounted_price__lt=10000)
  elif data=='above':
    mobiles=Product.objects.filter(category='M').filter(discounted_price__gt=10000)
  return render(request, 'app/mobile.html',{'mobiles': mobiles})

def laptop(request,data=None):
  brands=['APPLE','ASUS','Dell','HP','MSI']
  for b in brands:
    if data==None:
      laptops=Product.objects.filter(category='L')
    elif data==b:
      laptops=Product.objects.filter(category='L').filter(brand=data)
  if data=='below':
    laptops=Product.objects.filter(category='L').filter(discounted_price__lt=50000)
  elif data=='above':
    laptops=Product.objects.filter(category='L').filter(discounted_price__gt=50000)
  return render(request, 'app/laptop.html',{'laptops':laptops})

def television(request,data=None):
  brands=['Mi','Samsung','LG','HP','MSI']
  for b in brands:
    if data==None:
      televisions=Product.objects.filter(category='TV')
    elif data==b:
      televisions=Product.objects.filter(category='TV').filter(brand=data)
  if data=='below':
    televisions=Product.objects.filter(category='TV').filter(discounted_price__lt=20000)
  elif data=='above':
    televisions=Product.objects.filter(category='TV').filter(discounted_price__gt=20000)
  return render(request, 'app/television.html',{'televisions':televisions})

def headspeaker(request,data=None):
  if data==None:
    headspeakers=Product.objects.filter(category='HS')
  elif data=='below':
    headspeakers=Product.objects.filter(category='HS').filter(discounted_price__lt=1000)
  elif data=='above':
    headspeakers=Product.objects.filter(category='HS').filter(discounted_price__gt=1000)
  return render(request, 'app/headspeaker.html',{'headspeakers':headspeakers})

def topWear(request,data=None):
  if data==None:
    topwears=Product.objects.filter(category='TW')
  elif data=='below':
    topwears=Product.objects.filter(category='TW').filter(discounted_price__lt=500)
  elif data=='above':
    topwears=Product.objects.filter(category='TW').filter(discounted_price__gt=500)
  return render(request, 'app/topWear.html',{'topwears':topwears})

def bottomWear(request,data=None):
  if data==None:
    bottomwears=Product.objects.filter(category='BW')
  elif data=='below':
    bottomwears=Product.objects.filter(category='BW').filter(discounted_price__lt=500)
  elif data=='above':
    bottomwears=Product.objects.filter(category='BW').filter(discounted_price__gt=500)
  return render(request, 'app/bottomWear.html',{'bottomwears':bottomwears})

def watch(request,data=None):
  if data==None:
    watches=Product.objects.filter(category='W')
  elif data=='below':
    watches=Product.objects.filter(category='W').filter(discounted_price__lt=500)
  elif data=='above':
    watches=Product.objects.filter(category='W').filter(discounted_price__gt=500)
  return render(request, 'app/watch.html',{'watches':watches})

def buy_now(request,pk):
  if request.user.is_authenticated:
    user= request.user
    add= Customer.objects.filter(user=user)
    item= Product.objects.get(pk=pk)
    amount=item.discounted_price
    shipping= 70.0
    totalamount= amount+shipping
  return render(request, 'app/buynow.html',{'add':add,'item':item,'totalamount':totalamount})

def paymentdones(request,pk):
  user= request.user
  custid= request.GET.get('custid')
  customer= Customer.objects.get(id=custid)
  item= Product.objects.get(pk=pk)
  OrderPlaced(user=user,customer=customer,product=item).save()
  return HttpResponseRedirect('/orders')


def add_to_cart(request):
 if request.user.is_authenticated:
  user=request.user
  product_id=request.GET.get('prod_id')
  product=Product.objects.get(id=product_id)
  Cart(user=user,product=product).save()
  return HttpResponseRedirect('/showCart')
 else:
  return HttpResponseRedirect('/accounts/login/')
 
def showCart(request):
  if request.user.is_authenticated:
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping=70.0
    total_amount=0.0
    cart_product = [p for p in Cart.objects.all() if p.user==user]
    if cart_product:
      for p in cart_product:
        tempamount=(p.quantity*p.product.discounted_price)
        amount+=tempamount
        total_amount=amount+shipping
      return render(request,'app/showCart.html',{'carts':cart,'totalamount':total_amount,'amount':amount})
    else:
      return render(request,'app/emptycart.html') 
    
def plusCart(request):
  if request.method == 'GET':
    prod_id=request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    c.quantity+=1
    c.save()
    amount=0.0
    shipping=70.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
      tempamount=(p.quantity*p.product.discounted_price)
      amount+=tempamount
      totalamount=amount+shipping

  data = {
      'quantity' : c.quantity,
      'amount' : amount,
      'totalamount' : totalamount
    }  
  return JsonResponse(data) 

def minusCart(request):
  if request.method == 'GET':
    prod_id=request.GET['prod_id']
    c=Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
    if c.quantity > 1:
      c.quantity-=1
    c.save()
    amount=0.0
    shipping=70.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    for p in cart_product:
      tempamount=(p.quantity*p.product.discounted_price)
      amount+=tempamount
      totalamount=amount+shipping

  data = {
      'quantity' : c.quantity,
      'amount' : amount,
      'totalamount' : totalamount
    }  
  return JsonResponse(data)

def removeCart(request,id):
  if request.method == 'GET':
    c=Cart.objects.get(pk=id)
    c.delete()
    return HttpResponseRedirect('/showCart')
  
def checkout(request):
  if request.user.is_authenticated:
    user= request.user
    add= Customer.objects.filter(user=user)
    cart_items= Cart.objects.filter(user=user)
    amount= 0.0
    shipping= 70.0
    totalamount= 0.0
    cart_product = [p for p in Cart.objects.all() if p.user==request.user]
    if cart_product:
      for p in cart_product:
        tempamount= (p.quantity*p.product.discounted_price)
        amount+=tempamount
      totalamount= amount+shipping
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})
  else:
    return HttpResponseRedirect('/accounts/login')

def paymentdone(request,):
  user= request.user
  custid= request.GET.get('custid')
  customer= Customer.objects.get(id=custid)
  cart= Cart.objects.filter(user=user)
  for c in cart:
    OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
    c.delete()
  return HttpResponseRedirect('/orders')

def orders(request):
 if request.user.is_authenticated:
    op= OrderPlaced.objects.filter(user=request.user)
    return render(request, 'app/orders.html',{'op':op})
 else:
    return HttpResponseRedirect('/accounts/login')
 
def ordercancel(request,id):
  if request.method == 'GET':
    o=OrderPlaced.objects.get(pk=id)
    o.delete()
    return HttpResponseRedirect('/orders')

class ProfileView(View):
 def get(self,request):
  if request.user.is_authenticated:
    fm=CustomerProfileForm()
    return render(request, 'app/profile.html',{'form':fm,'active':'btn-primary'})
  else:
    return HttpResponseRedirect('/accounts/login')
 
 def post(self,request):
  if request.user.is_authenticated:
   fm=CustomerProfileForm(request.POST)
   if fm.is_valid():
     user=request.user
     name=fm.cleaned_data['name']
     locality=fm.cleaned_data['locality']
     city=fm.cleaned_data['city']
     zipcode=fm.cleaned_data['zipcode']
     state=fm.cleaned_data['state']
     reg=Customer(user=user,name=name,locality=locality,city=city,zipcode=zipcode,state=state)
     reg.save()
     messages.success(request,"Congratulations Profile Updated Successfully !!!")
     return HttpResponseRedirect('/profile/')
   return render(request, 'app/profile.html',{'form':fm,'active':'btn-primary'})
  else:
    return HttpResponseRedirect('/accounts/login')

def address(request):
 if request.user.is_authenticated:
  add=Customer.objects.filter(user=request.user)
  return render(request, 'app/address.html',{'address':add,'active':'btn-primary'})
 else:
   return HttpResponseRedirect('/accounts/login')

def delete_address(request,id):
  if request.method=='GET':
    add=Customer.objects.get(pk=id)
    add.delete()
    return HttpResponseRedirect('/address')


def user_changepass(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            fm=PasswordChange(user = request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                #This function is used for go to profile after password change
                update_session_auth_hash(request,fm.user)
                return HttpResponseRedirect('/passwordchangedone/')
        else:
            fm = PasswordChange(user = request.user)
        return render(request, 'app/changepassword.html',{'form':fm})
    else:
        return HttpResponseRedirect('/')
    
def passwordchangedone(request):
    return render(request,'app/passwordchangedone.html')


def log_in(request):
    if not request.user.is_authenticated:
        if request.method=="POST":
            fm = LoginForm(request=request, data=request.POST)
            if fm.is_valid():
                uname=fm.cleaned_data['username']
                upass=fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login (request,user)
                    return HttpResponseRedirect('/')
        else:
            fm = LoginForm()
        return render(request,'app/login.html', {'form':fm})
    else:
        return HttpResponseRedirect('/profile/')
    
def log_out(request):
    logout(request)
    return HttpResponseRedirect('/accounts/login/')


class CustomerRegistrationView(View):
  def get(self,request):
    fm=CustomerRegistrationForm()
    return render(request, 'app/customerregistration.html',{'form':fm})
  
  def post(self,request):
    fm=CustomerRegistrationForm(request.POST)
    if fm.is_valid():
      messages.success(request,"Registered Successfully")
      fm.save()
      return HttpResponseRedirect('/registration/')
    return render(request, 'app/customerregistration.html',{'form':fm})


def resetpassword(request):
  if request.method == 'POST':
    fm=PasswordReset(request.POST)
    if fm.is_valid():
      return HttpResponseRedirect('/resetpasswordconfirm/')
  else:
     fm = PasswordReset(request.POST)
  return render(request,'app/resetpassword.html',{'form':fm})

def resetPasswordConfirm(request):
  return render(request,'app/resetpasswordconfirm.html')

'''def resetPasswordDone(request):
  fm=SetPassword(request.POST)
  if fm.is_valid():
    return HttpResponseRedirect('/resetpasswordcomplete/')
  return render(request,'app/resetpassworddone.html',{'form':fm})'''

def resetPasswordDone(request,uidb64,token):
    if request.method == 'POST':
        fm = SetPassword(user=request.user, data=request.POST, uidb64=uidb64,token=token)
        if fm.is_valid():
            fm.save()
            # Updating the user's session after changing the password to avoid logouts.
            update_session_auth_hash(request, request.user)
            return HttpResponseRedirect('/resetpasswordcomplete/')
    else:
        fm = SetPassword(user=request.user)

    return render(request,'app/resetpassworddone.html',{'form':fm})

def resetPasswordComplete(request):
  return render(request,'app/resetpasswordcomplete.html')

#This project is build by Nilamber Singh Rajput