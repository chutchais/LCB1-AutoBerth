from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import (
    VoyListAPIView,
    VoyDetailAPIView,
    BerthListAPIView,
    VoyDetailAPIRedis,
    VoyListAPIRedis,
    TruckWindowListAPIView
    )

urlpatterns = [
    path('', VoyListAPIView.as_view(), name='voy_list'),
    # path('', VoyListAPIRedis, name='voy_list'),
	path('berth/', BerthListAPIView.as_view(), name='berth_list'),
    path('truck-window/', TruckWindowListAPIView.as_view(), name='truck-window'),
	# path('<slug>/', VoyDetailAPIView.as_view(), name='voy_detail'),
    path('<slug>/', VoyDetailAPIRedis, name='voy_detail'),

    # url(r'^$', VoyListAPIView.as_view(), name='voy_list'),
	# url(r'berth/$', BerthListAPIView.as_view(), name='berth_list'),
	# url(r'^(?P<slug>[\w-]+)/$', VoyDetailAPIView.as_view(), name='voy_detail'),

 #    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]