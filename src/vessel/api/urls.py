from django.conf.urls import url
from django.contrib import admin

from .views import (
    VesselListAPIView,
    VesselDetailAPIView
    )

urlpatterns = [
	url(r'^$', VesselListAPIView.as_view(), name='vessel_list'),
    url(r'^(?P<slug>[\w-]+)/$', VesselDetailAPIView.as_view(), name='vessel_detail'),
    # url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]