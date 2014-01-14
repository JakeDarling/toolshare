from django.conf.urls import patterns, url
from shed import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^addForm/$', views.addForm, name='addForm'),
    url(r'^add/$', views.add, name='add'),
    url(r'^viewSheds/$', views.viewSheds, name='viewSheds'),
    url(r'^removeShed/(?P<shed_id>\d+)/$', views.removeShed, name='removeShed'),
    url(r'^detailShed/(?P<shed_id>\d+)/$', views.detailShed, name='detailShed'),
    url(r'^editShed/(?P<shed_id>\d+)/$', views.editShed, name='editShed'),
)
