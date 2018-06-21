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
from django.shortcuts import render_to_response
from django.template import RequestContext
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
				filepath = request.FILES.get('filepath', False)
				if filepath:
					new_object.file = request.FILES['file']
				new_object.uploaded_at = localtime(now())
				new_object.save()
				order = Order.objects.get(name=data['name'],title = data['title'],prof_mail = data['prof_mail'])
				try:
					current_site = get_current_site(request)
					hash_prof = hashlib.md5(order.prof_mail)
					message =  "Dear Sir/Madam \r\n\r\n "+ data['name'] +" has submitted a Work request with you as the faculty Guide/Incharge.This Work request is awaiting your approval for further processing.Please click on the following link for detials and approval. \r\n\r\n" + current_site.domain + '/' + 'order_decision' +'/' + str(order.id) + '/' + hash_prof.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH CWS Work Request Approval'
					to_email = data['prof_mail']
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
					hash_mail = hashlib.md5(order.mail)
					message2 =  "Hello \r\n\r\n We have sucessfully recieved your Work request to Central Workshop.Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject2 = 'IITH CWS Work request'
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
	category = "ALL WORK REQUESTS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def unapproved_orders(request):
	orders = Order.objects.filter(approval3="Pending").order_by('-uploaded_at')
	category = "UNAPPROVED WORK REQUESTS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def pending_orders(request):
	orders = Order.objects.filter(approval3="Accepted").order_by('-uploaded_at')
	category = "PENDING WORK REQUESTS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def status_list(request):
	orders = Order.objects.filter(approval3="Accepted",completed=False).order_by('-uploaded_at')
	return render(request,'app/status_list.html',{'orders':orders})

def rejected_orders(request):
	orders = Order.objects.filter(approval3="Rejected").order_by('-uploaded_at')
	category = "REJECTED WORK REQUESTS"
	return render(request,'app/orders.html',{'orders':orders,'category':category})

def completed_orders(request):
	orders = Order.objects.filter(completed=True).order_by('-uploaded_at')
	category = "COMPLETED WORK REQUESTS"
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
				orders = Order.objects.filter(approval1 = 'Accepted',approval2='Accepted',approval3='Pending').order_by('-uploaded_at') | Order.objects.filter(approval1 = 'Accepted',approval2='May be',approval3='Pending').order_by('-uploaded_at')
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
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash,'approver':approver})
		elif (order.approval1 == 'Accepted' and approver.approver2 == user.username ):
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash,'approver':approver})
		elif (order.approval1 == 'Accepted' and (order.approval2 == 'Accepted' or order.approval2 == 'May be') and approver.approver3 == user.username):
			decisionform = DecisionForm()
			return render(request,'app/decision.html',{'order':order,'decisionform':decisionform,'prof_hash':prof_hash,'approver':approver})
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
				remarks = data['remarks']
				if decision == "Reject":					
					order.approval2 = 'Rejected'
					order.approval3 = 'Rejected'
					order.remarks2 = remarks
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Work request to CWS is rejected by Central Workshop Technical team.Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH CWS Work request'
					to_email = order.mail
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
				elif decision == "May be":
					data = decisionform.cleaned_data
					order.remarks2 = remarks
					order.approval2 = 'May be'
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Work request to CWS is marked as 'May be' by the Central Workshop Technical team.This means that they are not sure of the feasibility of the product.It is suggested that you meet the faculty incharge of Central Workshop for further discussion on the subject..Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH CWS Work request'
					to_email = order.mail
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
				else:					
					order.approval2 = 'Accepted'
					order.remarks2 = remarks
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Work request to CWS is accepted by Central Workshop Technical team.Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH CWS Work request'
					to_email = order.mail
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
				order.save()
				return HttpResponseRedirect("/approve_orders")
				# Your Workorder request to CWS is marked as 'May be' by the Central Workshop Technical team.This means they are not sure of the feasebility of the product.It is suggested that you meet the faculty incharge of Central Workshop for further discussion on the subject.
			else:
				return render(request,'app/decision.html',{'order':order,'decisionform':decisionform})
		elif (user.username == approver.approver3 and (order.approval2=='Accepted' or order.approval2=='May be') and order.approval1=='Accepted'):
			decisionform = DecisionForm(request.POST)
			if decisionform.is_valid():
				data = decisionform.cleaned_data
				decision = data['decision']
				remarks = data['remarks']
				if decision == "Reject":
					order.approval3 = 'Rejected'
					order.remarks3 = remarks
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Work request to CWS is rejected by Central Workshop Faculty Incharge.Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH CWS Work request'
					to_email = order.mail
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
				else:
					data = decisionform.cleaned_data
					remarks3 = data['remarks']
					order.remarks = remarks
					order.approval3 = 'Accepted'
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n Your Work request to CWS is approved by Central Workshop Faculty Incharge.Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH CWS Work request'
					to_email = order.mail
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
					remarks = data['remarks']
					order.approval1 = 'Rejected'
					order.approval2 = 'Rejected'
					order.approval3 = 'Rejected'
					order.remarks = remarks
				else:
					data = decisionform.cleaned_data
					remarks = data['remarks']
					order.remarks = remarks
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
					message =  "Hello \r\n\r\n Your Workshop request has been completed. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH CWS Work request'
					to_email = order.mail
					email = EmailMessage(mail_subject, message, to=[to_email])
					email.send()
				else:
					order.completed = False
					current_site = get_current_site(request)
					hash_mail = hashlib.md5(order.mail)
					message =  "Hello \r\n\r\n There is an update to your CWS Work request status.Please use below link for more detials and track the Work order status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
					mail_subject = 'IITH CWS Work request'
					to_email = order.mail
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
		remarks = data['remarks']
		if decision == "Reject":
			order.approval1 = 'Rejected'
			order.approval2 = 'Rejected'
			order.approval3 = 'Rejected'
			order.remarks1 = remarks
			current_site = get_current_site(request)
			hash_mail = hashlib.md5(order.mail)
			message =  "Hello \r\n\r\n Your Work request to CWS is rejected by the faculty Guide/Incharge.Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
			mail_subject = 'IITH CWS Work request'
			to_email = order.mail
			email = EmailMessage(mail_subject, message, to=[to_email])
			email.send()
		else:
			order.remarks1 = remarks
			order.approval1 = 'Accepted'
			current_site = get_current_site(request)
			hash_mail = hashlib.md5(order.mail)
			message =  "Hello \r\n\r\n Your Work request to CWS is approved by the faculty Guide/Incharge.Please use below link for more detials and track the Work request status. \r\n\r\n" + current_site.domain  + '/details'+'/' + str(order.id) + '/' + hash_mail.hexdigest() + '/' +  "\r\n\r\nThanking You\r\nIITH CWS\r\n"
			mail_subject = 'IITH CWS Workorder'
			to_email = order.mail
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
		return HttpResponse("Something went wrong !!!")


def handler404(request):
    response = render_to_response('404.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 404
    return response

def handler500(request):
    response = render_to_response('404.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 500
    return response







				




















