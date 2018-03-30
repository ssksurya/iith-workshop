from . import views
from django.conf.urls import include,url

urlpatterns = [
	url(r'^$', views.index),
	url(r'^form$', views.orders),
	url(r'^orders$', views.all_orders),
	url(r'^login$', views.login_menu),
	url(r'^do_login$', views.login),
	url(r'^do_register$', views.register),
]
