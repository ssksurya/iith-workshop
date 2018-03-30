# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import RequestContext
from django.shortcuts import render

from .forms import orderForm,LoginForm,RegisterForm 
from .models import Order

from django.contrib.auth.models import User
from django.utils.timezone import localtime, now
# Create your views here.

def index(request):
	return render(request,'app/index.html')

def order(request):
	if request.method == "POST":
		form = orderForm(request.POST,request.FILES)
		print form.errors
		if form.is_valid():
			try:
				data = form.cleaned_data
				new_object = Order()
				new_object.name = data['name']
				new_object.mail = data['mail']
				new_object.mobile = data['mobile']
				new_object.work = data['work']
				new_object.worktype = data['worktype']
				new_object.prof_name = data['prof_name']
				new_object.prof_mail = data['prof_mail']
				new_object.file = request.FILES['file']
				new_object.uploaded_at = localtime(now())
				new_object.save()
				return render(request,'app/index.html')
			except Exception as e:
				print(e)
				return render(request,'app/form.html',{'form':form})
		else:
			print 'errorr'
			return render(request,'app/form.html',{'form':form})
	else:
		form = orderForm() 
		return render(request,'app/form.html',{'form':form})

def all_orders(request):
	orders = Order.objects.all()
	print orders
	return render(request,'app/orders.html',{'orders':orders})

def login_menu(request):
	loginform = LoginForm()
	registerform = RegisterForm()
	return render(request,'app/login.html',{'loginform':loginform,'registerform':registerform})