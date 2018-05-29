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
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
import hashlib
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
				order = Order.objects.get(name=data['name'],title = data['title'],prof_mail = data['prof_mail'])
				try:
					current_site = get_current_site(request)
					hash_prof = hashlib.md5(order.prof_mail)
					message =  "Dear Sir/Madam \r\n\r\n You have a Workshop order to approve.Please click on the link below to find detials and approve it. \r\n\r\n" + current_site.domain + '/' + 'order_decision' +'/' + str(order.id) + '/' + hash_prof.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH Workshop Workorder Approval'
					to_email = data['prof_mail']
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
					hash_mail = hashlib.md5(order.mail)
					message2 =  "Hello \r\n\r\n You have submitted a Workshop order.Please use below link to find detials and track your order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject2 = 'IITH Workshop Workorder'
					to_email2 = data['mail']
					email = EmailMessage(mail_subject2, message2, to=[to_email2])
					email.send()
				except Exception,e:
					print str(e)
					order = Order.objects.get(name=data['name'],title = data['title'],prof_mail = data['prof_mail'])
					order.delete()
					message = "There is something wrong.Try again later"
					return render(request,'app/form.html',{'form':form,'message':message})
				return HttpResponseRedirect("/orders")
			except Exception as e:
				print e
				message = "There is something wrong.Try again later"
				return render(request,'app/form.html',{'form':form,'message':message})
		else:
			message = "There is something wrong with your form.Try again"
			return render(request,'app/form.html',{'form':form})
	else:
		form = orderForm() 
		return render(request,'app/form.html',{'form':form})

def all_orders(request):
	orders = Order.objects.all().order_by('-uploaded_at')
	category = "ALL ORDERS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def pending_orders(request):
	orders = Order.objects.filter(approval3="Pending").order_by('-uploaded_at')
	category = "PENDING ORDERS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def approved_orders(request):
	orders = Order.objects.filter(approval3="Accepted").order_by('-uploaded_at')
	category = "APPROVED ORDERS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def status_list(request):
	orders = Order.objects.filter(approval3="Accepted",completed=False).order_by('-uploaded_at')
	return render(request,'app/status_list.html',{'orders':orders})

def rejected_orders(request):
	orders = Order.objects.filter(approval3="Rejected").order_by('-uploaded_at')
	category = "REJECTED ORDERS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def completed_orders(request):
	orders = Order.objects.filter(completed=True).order_by('-uploaded_at')
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
				orders = Order.objects.filter(approval1 = 'Accepted',approval2='Pending').order_by('-uploaded_at')
			except:
				orders=[]
			return render(request,'app/approve_orders.html',{'orders':orders})
		elif (user.username == approver.approver3):
			try:
				orders = Order.objects.filter(approval1 = 'Accepted',approval2='Accepted',approval3='Pending').order_by('-uploaded_at')
			except:
				orders=[]
			return render(request,'app/approve_orders.html',{'orders':orders})
		else:
			try:
				orders = Order.objects.filter(prof_mail=user.username,approval1 = 'Pending').order_by('-uploaded_at')
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
		prof_hash = ""
		if (order.approval1 == 'Pending' and order.prof_mail == user.username ):
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash})
		elif (order.approval1 == 'Accepted' and approver.approver2 == user.username ):
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash})
		elif (order.approval1 == 'Accepted' and order.approval2 == 'Accepted' and approver.approver3 == user.username):
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash})
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
				if decision == "Reject":
					reason = data['reason']
					order.approval2 = 'Rejected'
					order.approval3 = 'Rejected'
					order.reason = reason
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Workshop order is rejected by Central Workshop.Please use below link to find detials and track your order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH Workshop Workorder'
					to_email = data['mail']
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
				else:
					data = decisionform.cleaned_data
					reason = data['reason']
					order.reason = reason
					order.approval2 = 'Accepted'
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Workshop order is approved by Central Workshop Staff.Please use below link to find detials and track your order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH Workshop Workorder'
					to_email = data['mail']
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
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
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Workshop order is rejected by Central Workshop Faculty Team.Please use below link to find detials and track your order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH Workshop Workorder'
					to_email = data['mail']
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
				else:
					data = decisionform.cleaned_data
					reason = data['reason']
					order.reason = reason
					order.approval3 = 'Accepted'
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Workshop order is approved by Central Workshop Faculty Team.Please use below link to find detials and track your order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH Workshop Workorder'
					to_email = data['mail']
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
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
					data = decisionform.cleaned_data
					reason = data['reason']
					order.reason = reason
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
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Workshop order has been completed.Please use below link to find detials and track your order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH Workshop Workorder'
					to_email = data['mail']
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
				else:
					order.completed = False
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n There is a update on your Workshop Order.Please use below link to find detials and track your order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH Workshop Workorder'
					to_email = data['mail']
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
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


def prof_decision_form(request,order_id,prof_hash):
	order = Order.objects.get(id= order_id)
	hash_object = hashlib.md5(order.prof_mail)
	if hash_object.hexdigest() == prof_hash:
		if order.approval1 == 'Pending':
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash})
		else:
			return HttpResponseRedirect("/orders")
	else:
		return HttpResponse("Something wrong")

def prof_decision(request,order_id,prof_hash):
	order = Order.objects.get(id= order_id)
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
			current_site = get_current_site(request)
			hash_mail = hashlib.md5(order.mail)
			message =  "Hello \r\n\r\n Your Workshop order is rejected by your reference professor.Please use below link to find detials and track your order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
			mail_subject = 'IITH Workshop Workorder'
			to_email = data['mail']
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
		else:
			order.reason = reason
			order.approval1 = 'Accepted'
			current_site = get_current_site(request)
			hash_mail = hashlib.md5(order.mail)
			message =  "Hello \r\n\r\n Your Workshop order is approved by your reference professor.Please use below link to find detials and track your order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
			mail_subject = 'IITH Workshop Workorder'
			to_email = data['mail']
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
		order.save()

		return render(request,'app/recorded.html')
	else:
		return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash})

def detail_hash(request,order_id,mail_hash):
	order = Order.objects.get(id= order_id)
	hash_object = hashlib.md5(order.mail)
	if hash_object.hexdigest() == mail_hash:
		status_list = Status.objects.filter(order=order_id)
		return render(request,'app/detail.html',{'order':order,'status_list':status_list})
	else:
		return HttpResponse("Something wrong")









				




















