from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import (
	ContainerListAPIView,
	ContainerDetailAPIView,
	ContainerUpdateAPIView
    )

urlpatterns = [
	path('', ContainerListAPIView.as_view(), name='list'),
	path('<slug>/', ContainerDetailAPIView.as_view(), name='detail'),
	path('<slug>/update/', ContainerUpdateAPIView.as_view(),name='update'),
	# url(r'^$', ContainerListAPIView.as_view(), name='list'),
	# url(r'^(?P<slug>[\w-]+)/$', ContainerDetailAPIView.as_view(), name='detail'),
	# url(r'^(?P<slug>[\w-]+)/update/$', ContainerUpdateAPIView.as_view(),name='update'),

]