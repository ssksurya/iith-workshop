# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Order, Approver
# Register your models here.

class DisplayOrder(admin.ModelAdmin):
	list_display = ('name','mail','mobile','title','work','worktype','work','file','prof_name','prof_mail','approval1','approval2','approval3','completed','reason')

class DisplayApprover(admin.ModelAdmin):
	list_display = ('approver2','approver3')

admin.site.register(Order, DisplayOrder)
admin.site.register(Approver, DisplayApprover)
