from django.db.models import Q

from rest_framework.generics import (
	CreateAPIView,
	DestroyAPIView,
	ListAPIView,
	UpdateAPIView,
	RetrieveAPIView,
	RetrieveUpdateAPIView
	)

from rest_framework.filters import (
	SearchFilter,
	OrderingFilter,
	)

from .serialize import VesselSerializer,VesselDetailSerializer
from berth.models import Vessel



class VesselListAPIView(ListAPIView):
	queryset=Vessel.objects.all()
	serializer_class=VesselSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['voy']
	# def get_queryset(self,*args,**kwargs):
	# 	# queryset_list=Comment.objects.filter(user=self.request.user)
	# 	queryset_list = Voy.objects.all()
	# 	from_date = self.request.GET.get("f")
	# 	to_date = self.request.GET.get("t")
	# 	print ('From : %s  -- To : %s ' % (from_date,to_date))
	# 	queryset_list = Voy.objects.filter(
	# 			Q(etb__range=[from_date,to_date])|
	# 			Q(etd__range=[from_date,to_date]))
	# 	return queryset_list

class VesselDetailAPIView(RetrieveAPIView):
	queryset=Vessel.objects.all()
	serializer_class=VesselDetailSerializer
	lookup_field='slug'
	print ("vessel details")
	# def get_queryset(self,*args,**kwargs):
	# 	# queryset_list=Comment.objects.filter(user=self.request.user)
	# 	queryset_list = Vessel.objects.all()
	# 	vessel_name = self.request.GET.get("name")
	# 	queryset_list = Vessel.objects.filter(
	# 			Q(name =vessel_name))
	# 	return queryset_list