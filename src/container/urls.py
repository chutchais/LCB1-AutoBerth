from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views
from .views import (ContainerListView,FileProcess,
					BayReport,BayDetail,ContainerDetailView,
					ContainerUpdateView,ContainerRestore,ContainerMove,BayRestore,BayReady,FileReady,FileUpdate,
                    MobileContainerUpdateView)

urlpatterns = [
    path('stowage/<slug>/restore', ContainerRestore,name='container-restore'), #Stowage Slug
    path('stowage/<slug>/move/<slot>', ContainerMove,name='container-move'), #Stowage Slug
    
    path('stowage/<slug>', ContainerUpdateView.as_view(),name='stowage'), #Stowage Slug

    path('<slug>/', BayReport, name='bay'), #File Slug
    
    path('<slug>/ready', FileReady, name='file-ready'), #File Slug
    path('<slug>/process', FileProcess,name='process'),
    path('<slug>/update', FileUpdate,name='update'),

    path('<slug>/<bay>/ready', BayReady, name='bay-ready'), #File Slug
    path('<slug>/<bay>/restore', BayRestore, name='bay-restore'), #File Slug
    path('<slug>/<bay>', BayDetail, name='detail'), #File Slug
    

    # url(r'stowage/(?P<slug>[-\w]+)/restore$', ContainerRestore,name='container-restore'), #Stowage Slug
    # url(r'stowage/(?P<slug>[-\w]+)/move/(?P<slot>[0-9]{6})$', ContainerMove,name='container-move'), #Stowage Slug
    
    # url(r'stowage/(?P<slug>[-\w]+)$', ContainerUpdateView.as_view(),name='stowage'), #Stowage Slug

    # url(r'(?P<slug>[-\w]+)/$', BayReport, name='bay'), #File Slug
    
    # url(r'(?P<slug>[-\w]+)/(?P<bay>\d+)/ready$', BayReady, name='bay-ready'), #File Slug
    # url(r'(?P<slug>[-\w]+)/(?P<bay>\d+)/restore$', BayRestore, name='bay-restore'), #File Slug
    # url(r'(?P<slug>[-\w]+)/(?P<bay>\d+)$', BayDetail, name='detail'), #File Slug
    
    # url(r'(?P<slug>[-\w]+)/ready$', FileReady, name='file-ready'), #File Slug
    # url(r'(?P<slug>[-\w]+)/process$', FileProcess,name='process'),
    # url(r'(?P<slug>[-\w]+)/update$', FileUpdate,name='update'),

]
