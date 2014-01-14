from django.conf.urls import patterns, url
from user import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^login/$', 'django.contrib.auth.views.login', 
    	{'template_name': 'user/login.html'}, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', 
    	{'next_page': '../'}, name='logout'),
	url(r'^register/$', views.addRegisterForm, name='registerForm'),
	url(r'^registerSubmit/$', views.register, name='registerSubmit'),
	url(r'^editInfo/$', views.editInfoForm, name='editInfo'),
	url(r'^editInfoSubmit/$', views.editInfo, name='editInfoSubmit'),
	url(r'^changePassword/$', 'django.contrib.auth.views.password_change', 
		{'template_name': 'user/changePassword.html',
		 'post_change_redirect': '../'}, name='changePassword'),
	url(r'^viewStatistics/$', views.viewStatistics, name='viewStatistics'),
	url(r'^editZipCode/$', views.editZipCode, name='editZipCode'),
)