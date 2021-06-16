from django.db.models import Q

from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView,
	RetrieveUpdateDestroyAPIView
	)

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from .serialize import BayPlanSerializer,BayPlanDetailSerializer,BayPlanUpdateSerializer
from bayplan.models import BayPlanFile



class BayPlanListAPIView(ListAPIView):
	queryset=BayPlanFile.objects.filter(uploaded=False,ready_to_load=True)
	serializer_class=BayPlanSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['filename']

class BayPlanDetailAPIView(RetrieveAPIView):
	queryset=BayPlanFile.objects.all()
	serializer_class=BayPlanDetailSerializer
	lookup_field='slug'
	# print ("vessel details")

class BayPlanUpdateAPIView(RetrieveUpdateDestroyAPIView):
	queryset=BayPlanFile.objects.all()
	serializer_class=BayPlanUpdateSerializer
	lookup_field='slug'



