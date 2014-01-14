from django.conf.urls import patterns, url
from tools import views
from django.conf import settings
from django.conf.urls.static import static

#from tools.views import ToolCreate, ToolUpdate, ToolDelete

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^addToolForm/$', views.addToolForm, name='addToolForm'),
    url(r'^addToolForm/(?P<id>\d+)/$', views.addToolForm, name='editForm'),
    url(r'^addTool/$', views.addTool, name='addTool'),
    url(r'^viewTools/$', views.viewTools, name='viewTools'),
    url(r'^viewMyTools/$', views.viewMyTools, name='viewMyTools'),
    url(r'^viewBorrowedTools/$', views.viewBorrowedTools, name='viewBorrowedTools'),
    url(r'^detail/(?P<tool_id>\d+)/$', views.detail, name='detail'),
    url(r'^remove/(?P<tool_id>\d+)/$', views.remove, name='remove'),
    url(r'^edit/(?P<tool_id>\d+)/$', views.editToolForm, name='editToolForm'),
    url(r'^editSubmit/(?P<tool_id>\d+)/$', views.editTool, name='editSubmit'),
    url(r'^borrowTool/(?P<tool_id>\d+)/$', views.borrowTool, name='borrowTool'),
    url(r'^borrowPrivateTool/(?P<tool_id>\d+)/(?P<borrower_id>\d+)/(?P<return_date>[\w\-]+)/(?P<timestamp>[\w\-;]+)/$', views.borrowPrivateTool, name='borrowPrivateTool'),
    url(r'^requestTool/(?P<tool_id>\d+)/$', views.borrowRequest, name='borrowRequest'),
    url(r'^denyForm/(?P<tool_id>\d+)/(?P<borrower_id>\d+)/(?P<timestamp>[\w\-;]+)/$', views.denyRequestForm, name='denyRequestForm'),
    url(r'^denyRequest/(?P<tool_id>\d+)/(?P<borrower_id>\d+)/(?P<timestamp>[\w\-;]+)/$', views.denyRequest, name='denyRequest'),
    url(r'^denyConfirmation/(?P<tool_id>\d+)/(?P<timestamp>[\w\-;]+)/$', views.denyReturnToolConfirmation, name='denyConfirmation'),
    url(r'^returnConfirmation/(?P<tool_id>\d+)/(?P<timestamp>[\w\-;]+)/$', views.returnToolConfirmation, name='returnConfirmation'),
    url(r'^returnTool/(?P<tool_id>\d+)/$', views.returnTool, name='returnTool'),
    url(r'^setAvailable/(?P<tool_id>\d+)/$', views.setAvailable, name='setAvailable'),
)