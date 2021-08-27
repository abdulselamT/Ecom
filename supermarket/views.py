from django.shortcuts import render,redirect
from.forms import *
from .models import *
from django.contrib.auth.models import Group
from django.contrib.auth import authenticate, login, logout

from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.

def homepage(request):
	products=Product.objects.all()
	totalcart=len(Order.objects.filter(added=True))
	context={'products':products,'tot':totalcart}
	return render(request,'supermarket/store.html',context)
@login_required(login_url='login')
def cart(request):
	orders=Order.objects.filter(added=True).filter(customer=request.user.customer)
	total=sum([k.calc_total() for k in orders])
	print(total)
	context={"orders":orders,'total':total,'size':len(orders)}
	return render(request,'supermarket/cart.html',context)
@login_required(login_url='login')
def checkout(request):
	orders=Order.objects.filter(added=True).filter(customer=request.user.customer)
	total=sum([k.calc_total() for k in orders])
	context={'orders':orders,'total':total,'size':len(orders)}
	return render(request,'supermarket/checkout.html',context)
@unauthenticated_user
def registercustomer(request):
	form=CreateUserForm()
	customerform=CustomerForm()
	print("working1")
	if request.method=="POST":
		form=CreateUserForm(request.POST)
		customerform=CustomerForm(request.POST,request.FILES)
		print("working2")
		if form.is_valid() and customerform.is_valid():
			group=Group.objects.get(name='customer')
			user=form.save()
			user.groups.add(group)
			customer=customerform.save(commit=False)
			print("working3")
			customer.user=user
			customer.save()
			y=Product.objects.all()
			for k in y:
				Order.objects.create(customer=Customer.objects.last(),product=k)
				print("order is running")
			return redirect('store')
	context={"form":form,"customerform":customerform}
	return render(request,'supermarket/register.html',context)

def registerproduct(request):
	form = ProductForm()
	if request.method=="POST":
		form=ProductForm(request.POST,request.FILES)
		if form.is_valid():
			form.save()
			y=Customer.objects.all()
			for k in y:
				Order.objects.create(product=Product.objects.last(),customer=k)
				print("order is running")
			return redirect('store')
	context={'form':form}
	return render(request,'supermarket/register.html',context)
@unauthenticated_user
def loginPage(request):

	if request.method == 'POST':
		username = request.POST.get('username')
		password =request.POST.get('password')

		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			return redirect('/')
		else:
			messages.info(request, 'Username OR password is incorrect')

	context = {}
	return render(request, 'supermarket/login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('login')

@login_required(login_url='login')
def addtocart(requiest,pk):
	x=Product.objects.get(id=pk)
	y=Order.objects.filter(product=x).get(customer=requiest.user.customer)
	print(y)
	print(y.added)
	if y.added:
		y.added=False
		y.save()
		
	else:
		y.added=True
		y.save()
	return redirect('store')
@login_required(login_url='login')
def addup(request,pk):
	x=Product.objects.get(id=pk)
	y=Order.objects.filter(product=x).get(customer=request.user.customer)
	y.tot+=1
	y.save()
	return redirect('cart')
@login_required(login_url='login')
def adddown(request,pk):
	x=Product.objects.get(id=pk)
	y=Order.objects.filter(product=x).get(customer=request.user.customer)
	if y.tot>=2:
		y.tot-=1
	else:
		y.added=False
	y.save()
	return redirect('cart')
@login_required(login_url='login')
def finish_transaction(request):
	orders=Order.objects.filter(added=True).filter(customer=request.user.customer)
	total=sum([k.calc_total() for k in orders])
	x=Customer.objects.get(id=request.user.customer.id)
	if x.total_birr>=total:
		x.total_birr-=total
	else:
		return render(request,'supermarket/checkout.html',{'error':"sorry you have ensufficent balance you need "+str(total-x.total_birr)+" more Birr"})
	x.save()
	itemss=[]
	itemss=set(itemss)
	y=Historypurchase.objects.create(customer=request.user.customer,total_cost=total)
	for ab in orders:
		y.items.add(ab.product)
		ab.added=False
		ab.save()
	print(x.total_birr)
	context={"finished" :"thanks you have finished willdeliver to"}
	return render(request,'supermarket/checkout.html',context)