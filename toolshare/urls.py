from django.conf.urls import patterns, include, url
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'toolshare.views.home', name='home'),
    # url(r'^toolshare/', include('toolshare.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
   	url(r'^admin/', include(admin.site.urls)),
   	url(r'^', include('user.urls')),
        url(r'^tools/', include('tools.urls', namespace="tools")),
        url(r'^shed/', include('shed.urls', namespace="shed")),
        url(r'^notifications/', include('notifications.urls', namespace='notifications')),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

                       
)
