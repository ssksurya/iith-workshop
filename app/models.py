# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
STATUS_CHOICES = (
	('Accepted','Accepted'),
	('Rejected','Rejected'),
	('Pending','Pending'),
	('May be','May be'),
)
class Order(models.Model):
	name = models.TextField(max_length=100,blank=True)
	mail = models.TextField(max_length=100,blank=True)
	mobile = models.BigIntegerField()
	work = models.TextField(max_length=500,blank=True)
	worktype = models.TextField(max_length=20,blank=True)
	title = models.TextField(max_length=100,blank=True)
	file = models.FileField(upload_to='orders/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	prof_name = models.TextField(max_length=100,blank=True)
	prof_mail = models.TextField(max_length=100,blank=True)
	approval1 = models.CharField(max_length=10, choices=STATUS_CHOICES,default='Pending')
	approval2 = models.CharField(max_length=10, choices=STATUS_CHOICES,default='Pending')
	approval3 = models.CharField(max_length=10, choices=STATUS_CHOICES,default='Pending')
	completed = models.BooleanField(default=False)
	remarks1 = models.TextField(max_length=1000,blank=True)
	remarks2 = models.TextField(max_length=1000,blank=True)
	remarks3 = models.TextField(max_length=1000,blank=True)

class Approver(models.Model):
	approver2 = models.TextField(max_length=100)
	approver3 = models.TextField(max_length=100)

class Status(models.Model):
	order = models.IntegerField()
	status_text = models.TextField(max_length=1000,blank=True)
	uploaded_at = models.DateTimeField(auto_now_add=True)

	

