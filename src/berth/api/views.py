from django.db.models import Q

import redis
db = redis.StrictRedis('berth-redis', 6379,db=0, charset="utf-8", decode_responses=True) #Production

from django_q.tasks import async_task

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

from .serialize import VoySerializer,VoyDetailSerializer,BerthSerializer,TruckWindowSerializer
from berth.models import Voy


class BerthListAPIView(ListAPIView):
	queryset=Voy.objects.all()
	serializer_class=BerthSerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['vessel__name','voy','code']

	def get_queryset(self,*args,**kwargs):
		import datetime
		from datetime import timedelta
		today= datetime.date.today()
		from_date = today - timedelta(days=7)
		to_date = today +  timedelta(days=14)
		# from_date 	= '2019-03-20'
		# to_date 	= '2019-03-25'
		queryset_list = Voy.objects.filter(
				Q(etb__range=[from_date,to_date])|
				Q(etd__range=[from_date,to_date])).exclude(terminal__name='B2').order_by('etb')
		return queryset_list



class VoyListAPIView(ListAPIView):
	# queryset=Voy.objects.all()
	serializer_class=VoySerializer
	filter_backends=[SearchFilter,OrderingFilter]
	search_fields =['voy']
	def get_queryset(self,*args,**kwargs):
		# queryset_list=Comment.objects.filter(user=self.request.user)
		queryset_list = Voy.objects.all()
		from_date = self.request.GET.get("f")
		to_date = self.request.GET.get("t")
		terminal = self.request.GET.get("terminal")
		print(f'VoyListAPIView : from {from_date}  to {to_date} on terminal {terminal} ')
		# print ('From : %s  -- To : %s ' % (from_date,to_date))
		# print ('Terminal %s' % terminal)
		if terminal :
			queryset_list = Voy.objects.filter(
				Q(etb__range=[from_date,to_date])|
				Q(etd__range=[from_date,to_date]),terminal__name__icontains=terminal).order_by('etb')
		else:
			queryset_list = Voy.objects.filter(
					Q(etb__range=[from_date,to_date])|
					Q(etd__range=[from_date,to_date])).order_by('etb')
		return queryset_list
from django.http import JsonResponse
import json
def VoyListAPIRedis(request):
	from_date 	= request.GET.get("f")
	to_date 	= request.GET.get("t")
	terminal 	= request.GET.get("terminal")
	if terminal :
		queryset_list = Voy.objects.filter(
			Q(etb__range=[from_date,to_date])|
			Q(etd__range=[from_date,to_date]),terminal__name__icontains=terminal).order_by('etb')
	else:
		queryset_list = Voy.objects.filter(
				Q(etb__range=[from_date,to_date])|
				Q(etd__range=[from_date,to_date])).order_by('etb')
	
	payloads = []
	payloads= [json.loads(get_voy_json(x.slug)) for x in queryset_list]
	
	return JsonResponse(payloads,safe=False)
	
	

class VoyDetailAPIView(RetrieveAPIView):
	queryset=Voy.objects.all()
	serializer_class=VoyDetailSerializer
	lookup_field='slug'


def VoyDetailAPIRedis(request,slug):
	## Check on Redis(db=0)
	# key=slug
	# if db.exists(slug):
	# 	source_data ='Redis'
	# 	payload = db.get(slug)
	# else:
	# 	voy = Voy.objects.get(slug=key)
	# 	async_task("berth.services.save_voy_to_redis",voy)
	# 	payload = voy.json
	# 	source_data ='Database'
	payload = get_voy_json(slug)

	print(f'VoyDetailAPIRedis of {slug} from ...')
	return JsonResponse(json.loads(payload),safe=False)
	# pass

def get_voy_json(slug):
	from berth.models import Voy
	key=slug
	if db.exists(slug):
		source_data ='Redis'
		payload = db.get(slug)
	else:
		voy = Voy.objects.get(slug=key)
		async_task("berth.services.save_voy_to_redis",voy)
		payload = voy.json
		source_data ='Database'
	return payload

# Added on 
# def truck_window(request,week=2):
# 	from django.db.models import Q
# 	from django.db.models import Max
# 	import datetime
# 	from datetime import timedelta
# 	# Use current week
# 	today= datetime.date.today()
# 	from_date = today -  timedelta(days=today.weekday())
# 	to_date = from_date +  timedelta(days=week*7)
# 	# year = to_date.strftime('%Y')#-%m-%d %H:%M
# 	# workweek = today.isocalendar()[1]
# 	print (f'Truck window From date : {from_date} To date : {to_date}')

# 	voys = Voy.objects.filter(
# 		Q(etb__range=[from_date,to_date]),
# 		vessel__v_type='VESSEL',
# 		draft=False
# 		).exclude(load_no=0,terminal = 'B2').order_by('etb')
# 	payloads={'from':from_date,
# 			'to':to_date}
# 	return JsonResponse(payloads,safe=False)

class TruckWindowListAPIView(ListAPIView):
	queryset			=	Voy.objects.all()
	serializer_class	=	TruckWindowSerializer
	filter_backends		=	[SearchFilter,OrderingFilter]
	# search_fields =['vessel__name','voy','code']

	def get_queryset(self,*args,**kwargs):
		import datetime
		from datetime import timedelta
		today		= datetime.date.today()
		from_date 	= today -  timedelta(days=today.weekday())
		to_date 	= today +  timedelta(days=14)
		queryset_list = Voy.objects.filter(
				Q(etb__range=[from_date,to_date]),
				vessel__v_type='VESSEL',
				draft=False
				).exclude(terminal__name='B2').order_by('etb')
		return queryset_list