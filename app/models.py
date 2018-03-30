# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Order(models.Model):
	name = models.TextField(max_length=100,blank=True)
	mail = models.TextField(max_length=100,blank=True)
	mobile = models.IntegerField()
	work = models.TextField(max_length=1000,blank=True)
	worktype = models.TextField(max_length=20,blank=True)
	work = models.TextField(max_length=1000,blank=True)
	file = models.FileField(upload_to='orders/')
	uploaded_at = models.DateTimeField(auto_now_add=True)
	prof_name = models.TextField(max_length=100,blank=True)
	prof_mail = models.TextField(max_length=100,blank=True)
	approval1 = models.BooleanField(default=False)
	approval2 = models.BooleanField(default=False)
	approval3 = models.BooleanField(default=False)
	completed = models.BooleanField(default=False)
	

