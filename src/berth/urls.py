from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views
from .views import VoyDetailView,CutOffDetailView,CutOffUpdateView, \
        CutOffCreateView,CutOffDeleteView,truckWindow

urlpatterns = [
    path('', views.index, name='index'),
    path('voy/<slug>/', VoyDetailView.as_view(), name='voy-detail'),
    path('cutoff/<pk>/delete/', CutOffDeleteView.as_view(), name='cutoff-delete'),
    path('cutoff/<pk>/', CutOffUpdateView.as_view(), name='cutoff-detail'),
    path('voy/<slug>/create/',CutOffCreateView.as_view(),name='cutoff-create'),
    path('cutoff/',views.cutoff, name='cutoff-home'),
    path('export/',views.export, name='export'),
    path('etb/<vessel_code>/<voy>/',views.etb, name='etb'),
    # Added on April 26,2021
    path('etd/<vessel_code>/<voy>/',views.etd, name='etd'),
    path('truckwindow/',views.truckWindow, name='truck-window'),
    # url(r'^$', views.index, name='index'),
    # url(r'voy/(?P<slug>[-\w]+)/$', VoyDetailView.as_view(), name='voy-detail'),
    # url(r'cutoff/(?P<pk>\d+)/delete/$', CutOffDeleteView.as_view(), name='cutoff-delete'),
    # url(r'cutoff/(?P<pk>\d+)/$', CutOffUpdateView.as_view(), name='cutoff-detail'),
    # url(r'voy/(?P<slug>[-\w]+)/create/$',CutOffCreateView.as_view(),name='cutoff-create'),
    # url(r'cutoff/$',views.cutoff, name='cutoff-home'),
    # url(r'export/$',views.export, name='export'),
    # url(r'etb/(?P<vessel_code>[-\w]+)/(?P<voy>[-\w]+)/$',views.etb, name='etb'),
]

admin.site.site_header = 'Auto Berth Schedule'