from . import views
from django.conf.urls import include,url
from django.contrib.auth.views import logout
from django.conf.urls.static import static

urlpatterns = [
	url(r'^$', views.index),
	url(r'^form$', views.order),
	url(r'^form$', views.order),
	url(r'^orders$', views.all_orders),
	url(r'^unapproved_orders$', views.unapproved_orders),
	url(r'^pending_orders$', views.pending_orders),
	url(r'^completed_orders$', views.completed_orders),
	url(r'^rejected_orders$', views.rejected_orders),
	url(r'^status_list$', views.status_list),
	url(r'^status_completed_list$', views.status_completed_list),
	url(r'^login/$', views.login_menu),
	url(r'^do_login$', views.do_login),
	url(r'^do_register$', views.do_register),
	url(r'logout', logout, {'next_page': '/'}),
	url(r'^approve_orders$', views.approve_orders),
	url(r'^detail/(?P<order_id>[0-9]+)/$',views.detail),
	url(r'^order_decision/(?P<order_id>[0-9]+)/$',views.decision_input),
	url(r'^decision/(?P<order_id>[0-9]+)/$', views.decision),
	url(r'^update_status/(?P<order_id>[0-9]+)/$', views.update_status),
	url(r'^order_decision/(?P<order_id>[0-9]+)/(?P<prof_hash>[0-9A-Za-z_\-]+)/$',views.prof_decision_form),
	url(r'^decision/(?P<order_id>[0-9]+)/(?P<prof_hash>[0-9A-Za-z_\-]+)$', views.prof_decision),
	url(r'^details/(?P<order_id>[0-9]+)/(?P<mail_hash>[0-9A-Za-z_\-]+)/$', views.detail_hash),
] 

handler404 = 'app.views.handler404'
handler500 = 'app.views.handler500'
