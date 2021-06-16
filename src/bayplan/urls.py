from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from . import views
from .views import BayPlanCreateView,VoyDetailView,BayPlanDeleteView,BayPlanUpdateView

urlpatterns = [
    path('', views.index, name='index'),
    path('<slug>/', VoyDetailView.as_view(), name='voy-detail'),
    path('<slug>/create', BayPlanCreateView.as_view(),name='create'),
    path('<slug>/delete', BayPlanDeleteView.as_view(),name='delete'),
    path('<slug>/edit', BayPlanUpdateView.as_view(),name='edit'),
    path('<slug>/container', BayPlanUpdateView.as_view(),name='container'),
    # url(r'^$', views.index, name='index'),
    # url(r'(?P<slug>[-\w]+)/$', VoyDetailView.as_view(), name='voy-detail'),
    # url(r'(?P<slug>[-\w]+)/create$', BayPlanCreateView.as_view(),name='create'),
    # url(r'(?P<slug>[-\w]+)/delete$', BayPlanDeleteView.as_view(),name='delete'),
    # url(r'(?P<slug>[-\w]+)/edit$', BayPlanUpdateView.as_view(),name='edit'),
    # url(r'(?P<slug>[-\w]+)/container$', BayPlanUpdateView.as_view(),name='container'),

]

admin.site.site_header = 'Auto Berth Schedule'
