from django.conf.urls import patterns, url
from notifications import views

urlpatterns = patterns('',
    url(r'^log_notification$', views.log_notification, name='log_notification'),
    url(r'^view/$', views.view_notifications, name='view_notifications'),
    url(r'^view_more/(?P<counter>\d+)$', views.view_more, name='view_more')

)