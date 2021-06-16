from django.db.models import Q,F

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

from .serialize import ContainerListSerializer,ContainerDetailSerializer,ContainerUpdateSerializer
from container.models import Container



class ContainerListAPIView(ListAPIView):
	queryset=Container.objects.all()
	serializer_class=ContainerListSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['container']

	# def get_queryset(self):
	# 	return Container.objects.all().exclude(stowage=F('original_stowage'))


class ContainerDetailAPIView(RetrieveAPIView):
	queryset=Container.objects.all()
	serializer_class=ContainerDetailSerializer
	lookup_field='slug'
	# print ("vessel details")

class ContainerUpdateAPIView(RetrieveUpdateDestroyAPIView):
	queryset=Container.objects.all()
	serializer_class=ContainerUpdateSerializer
	lookup_field='slug'



