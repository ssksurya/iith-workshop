# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

from .forms import orderForm,LoginForm,RegisterForm , DecisionForm , StatusForm
from .models import Order, Approver , Status

from django.contrib.auth.models import User
from django.utils.timezone import localtime, now
# Create your views here.

def index(request):
	approver = Approver.objects.all()
	approver = approver[0]
	return render(request,'app/index.html',{'approver':approver})

def order(request):
	if request.method == "POST":
		form = orderForm(request.POST,request.FILES)
		if form.is_valid():
			try:
				data = form.cleaned_data
				new_object = Order()
				new_object.name = data['name']
				new_object.mail = data['mail']
				new_object.mobile = data['mobile']
				new_object.title = data['title']
				new_object.work = data['work']
				new_object.worktype = data['worktype']
				new_object.prof_name = data['prof_name']
				new_object.prof_mail = data['prof_mail']
				new_object.file = request.FILES['file']
				new_object.uploaded_at = localtime(now())
				new_object.save()
				return render(request,'app/index.html')
			except Exception as e:
				return render(request,'app/form.html',{'form':form})
		else:
			return render(request,'app/form.html',{'form':form})
	else:
		form = orderForm() 
		return render(request,'app/form.html',{'form':form})

def all_orders(request):
	orders = Order.objects.all()
	category = "ALL ORDERS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def pending_orders(request):
	orders = Order.objects.filter(approval3="Pending")
	category = "PENDING ORDERS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def approved_orders(request):
	orders = Order.objects.filter(approval3="Accepted")
	category = "APPROVED ORDERS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def status_list(request):
	orders = Order.objects.filter(approval3="Accepted",completed=False)
	return render(request,'app/status_list.html',{'orders':orders})

def rejected_orders(request):
	orders = Order.objects.filter(approval3="Rejected")
	category = "REJECTED ORDERS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def completed_orders(request):
	orders = Order.objects.filter(completed=True)
	category = "COMPLETED ORDERS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})


def login_menu(request):
	loginform = LoginForm()
	registerform = RegisterForm()
	return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform})

def do_login(request):
	if request.method == "POST":
		loginform = LoginForm(request.POST)
		if loginform.is_valid():
			data = loginform.cleaned_data
			username = data['username']
			password = data['password']
			user = authenticate(username=username,password=password)
			
			if user is not None:
				login(request, user)
				return HttpResponseRedirect("/")
			else:
				registerform = RegisterForm()
				message = "User doesn't exists or Password is incorrect"
				return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform,'message':message})
		else:
			registerform = RegisterForm()
			message = "Please enter coreect details"
			return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform,'message':message})
	else:
		loginform = LoginForm()
		registerform = RegisterForm()
		return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform})

def do_register(request):
	if request.method == "POST":
		registerform = RegisterForm(request.POST)
		if registerform.is_valid():
			data = registerform.cleaned_data
			username = data['username']
			password1 = data['password1']
			password2 = data['password2']
			user = registerform.save(commit=False)
			if password1 == password2:
				user.set_password(password1)
				user.save()
				login(request, user)
				return HttpResponseRedirect("/")
			else:
				loginform = LoginForm()
				message = "Password don;t match"
				return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform,'message':message})
		else:
			loginform = LoginForm()
			message = "User already exists"
			return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform,'message':message})
	else:
		loginform = LoginForm()
		registerform = RegisterForm()
		return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform})

def approve_orders(request):
	if request.user.is_authenticated():
		user = request.user
		approver = Approver.objects.all()
		approver = approver[0]
		if (user.username == approver.approver2):
			try:
				orders = Order.objects.filter(approval1 = 'Accepted',approval2='Pending')
			except:
				orders=[]
			return render(request,'app/approve_orders.html',{'orders':orders})
		elif (user.username == approver.approver3):
			try:
				orders = Order.objects.filter(approval1 = 'Accepted',approval2='Accepted',approval3='Pending')
			except:
				orders=[]
			return render(request,'app/approve_orders.html',{'orders':orders})
		else:
			try:
				orders = Order.objects.filter(prof_mail=user.username,approval1 = 'Pending')
			except:
				orders=[]
			return render(request,'app/approve_orders.html',{'orders':orders})
	else:
		return HttpResponseRedirect("/login")

def decision_input(request,order_id):
	if request.user.is_authenticated():
		user = request.user
		order = Order.objects.get(id=order_id)
		approver = Approver.objects.all()
		approver = approver[0]
		if (order.approval1 == 'Pending' and order.prof_mail == user.username ):
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform})
		elif (order.approval1 == 'Accepted' and approver.approver2 == user.username ):
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform})
		elif (order.approval1 == 'Accepted' and order.approval2 == 'Accepted' and approver.approver3 == user.username):
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform})
		else:
			return HttpResponseRedirect("/approve_orders")
	else:
		return HttpResponseRedirect("/orders")

def detail(request,order_id):
	order = Order.objects.get(id=order_id)
	status_list = Status.objects.filter(order=order_id)
	return render(request,'app/detail.html',{'order':order,'status_list':status_list})
	
def decision(request,order_id):
	if request.user.is_authenticated():
		user = request.user
		order = Order.objects.get(id=order_id)
		approver = Approver.objects.all()
		approver = approver[0]
		if (user.username == approver.approver2 and order.approval1=='Accepted'):
			decisionform = DecisionForm(request.POST)
			if decisionform.is_valid():
				data = decisionform.cleaned_data
				decision = data['decision']
				print decision
				if decision == "Reject":
					reason = data['reason']
					order.approval2 = 'Rejected'
					order.approval3 = 'Rejected'
					order.reason = reason
				else:
					order.approval2 = 'Accepted'
				order.save()
				return HttpResponseRedirect("/approve_orders")
			else:
				return render(request,'app/decision.html',{'order':order,'decisionform':decisionform})
		elif (user.username == approver.approver3 and order.approval1==	'Accepted' and order.approval2=='Accepted'):
			decisionform = DecisionForm(request.POST)
			if decisionform.is_valid():
				data = decisionform.cleaned_data
				decision = data['decision']
				if decision == "Reject":
					reason = data['reason']
					order.approval3 = 'Rejected'
					order.reason = reason
				else:
					order.approval3 = 'Accepted'
				order.save()
				return HttpResponseRedirect("/approve_orders")
			else:
				return render(request,'app/decision.html',{'order':order,'decisionform':decisionform})
		elif(user.username == order.prof_mail and order.approval1 == 'Pending'):
			decisionform = DecisionForm(request.POST)
			if decisionform.is_valid():
				data = decisionform.cleaned_data
				decision = data['decision']
				if decision == "Reject":
					reason = data['reason']
					order.approval1 = 'Rejected'
					order.approval2 = 'Rejected'
					order.approval3 = 'Rejected'
					order.reason = reason
				else:
					order.approval1 = 'Accepted'
				order.save()
				return HttpResponseRedirect("/approve_orders")
			else:
				return render(request,'app/decision.html',{'order':order,'decisionform':decisionform})

		else:
			return HttpResponseRedirect("/approve_orders")
	else:
		return HttpResponseRedirect("/orders")

def update_status(request,order_id):
	if request.user.is_authenticated:
		order = Order.objects.get(id=order_id)
		if request.method == "POST":
			statusform = StatusForm(request.POST)
			if statusform.is_valid():
				data = statusform.cleaned_data
				
				status_input = data['status_input']
				completed_input = data['completed_input']
				new_object = Status()
				new_object.order = order_id
				new_object.status_text = status_input
				if completed_input=="Yes":
					order.completed = True
				else:
					order.completed = False
				new_object.save()
				order.save()
				return HttpResponseRedirect("/status_list")
			else:
				return render(request,'app/status_form.html',{'statusform':statusform})
		else:
			statusform = StatusForm()
			return render(request,'app/status_form.html',{'statusform':statusform,'order':order})
	else:
		return HttpResponseRedirect("/login")








				




















