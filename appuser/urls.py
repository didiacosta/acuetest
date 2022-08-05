from django.conf.urls import url

from . import views

urlpatterns = [
	url(r'^login/$', views.login_view, name='appuser.login'),
	url(r'^home/$', views.home_view, name='appuser.home'),
	url(r'^logout/$', views.logout_view, name='appuser.logout'),
]