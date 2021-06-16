from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from .views import (
	BayPlanListAPIView,
	BayPlanDetailAPIView,
	BayPlanUpdateAPIView
    )

urlpatterns = [
	path('', BayPlanListAPIView.as_view(), name='bayfile_list'),
	path('<slug>/', BayPlanDetailAPIView.as_view(), name='bayfile_detail'),
	path('<slug>/update/', BayPlanUpdateAPIView.as_view(),name='update'),
	# url(r'^$', BayPlanListAPIView.as_view(), name='bayfile_list'),
	# url(r'^(?P<slug>[\w-]+)/$', BayPlanDetailAPIView.as_view(), name='bayfile_detail'),
	# url(r'^(?P<slug>[\w-]+)/update/$', BayPlanUpdateAPIView.as_view(),name='update'),

]