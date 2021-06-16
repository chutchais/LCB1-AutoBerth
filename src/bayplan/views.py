from django.shortcuts import render

# Create your views here.
# from pdfdocument.utils import pdf_response 
# from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
# from django.core.urlresolvers import reverse
from django.urls import reverse

import os.path
from django.conf import settings

from berth.models import Voy

from django.shortcuts import get_object_or_404
from django.views.generic import View,ListView,DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect

from .forms import BayPlanForm
from .models import BayPlanFile

class BayPlanUpdateView(LoginRequiredMixin,UpdateView):
	model = BayPlanFile
	template_name = 'bayplan/bayplan_detail_update.html'
	form_class = BayPlanForm

	def get_queryset(self):
		qs = super(BayPlanUpdateView, self).get_queryset()
		return qs.all()

	def get_form_kwargs(self):
		kwargs = super(BayPlanUpdateView,self).get_form_kwargs()
		print(kwargs)
		return kwargs

class BayPlanCreateView(LoginRequiredMixin,CreateView):
	template_name = 'form.html'
	form_class = BayPlanForm
	success_url='/bayplan'

	def form_valid(self,form):
		print ('=====================Slug %s' % self.kwargs.get('slug'))
		voy = get_object_or_404(Voy, slug=self.kwargs.get('slug'))
		print (voy)
		form.instance.voy = voy
		# form.instance.filename = request.FILES['file']
		obj = form.save(commit=False)
		return super(BayPlanCreateView,self).form_valid(form)

	def get_initial(self):
		# print ('get_initial %s' % self.kwargs)
		voy = get_object_or_404(Voy, slug=self.kwargs.get('slug'))
		return {'voy':voy}

	def get_form_kwargs(self):
		kwargs = super(BayPlanCreateView,self).get_form_kwargs()
		# print (kwargs)
		# kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
		# print ('Kwarg %s' % self.request)
		return kwargs

	def get_success_url(self,*args, **kwargs):
		slug =self.object.voy.slug
		print(slug)
		url = reverse('bayplan:voy-detail',kwargs={'slug':slug})
		return url
		# reverse_lazy('container:detail',kwargs={'slug':slug,'bay':bay},query={'q':self.object.container})
		# return reverse(url)


	def get_queryset(self):
		qs = super(BayPlanCreateView, self).get_queryset()
		return qs.filter(voy__vessel__v_type='VESSEL')

	def get_context_data(self,*args,**kwargs):
		context = super(BayPlanCreateView,self).get_context_data(*args,**kwargs)
		context['title']='Upload Bay plan file'
		# context['voy']= 'Add Cut-Off Datetime'
		return context


class BayPlanDeleteView(LoginRequiredMixin,DeleteView):
	model = BayPlanFile
	success_url = reverse_lazy('bayplan:index')

	def get_object(self, queryset=None):
		obj = super(BayPlanDeleteView, self).get_object()
		# print ('Delete %s' % obj)
		return obj

	def get_success_url(self):
	# Assuming there is a ForeignKey from Comment to Post in your model
		voy = self.object.voy 
		print (voy)
		return reverse_lazy( 'bayplan:voy-detail', kwargs={'slug': voy.slug})


class VoyDetailView(LoginRequiredMixin,DetailView):
	model = Voy
	template_name = 'bayplan/bayplan_voy_detail.html'


def foo(year, week):
	from datetime import date, timedelta
	d = date(year,1,1)
	dlt = timedelta(days = ((week-1)*7)+1)
	return d + dlt ,  d + dlt + timedelta(days=7)
	
def index(request):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

		
	from django.db.models import Q
	from django.db.models import Max
	# from datetime import datetime
	import datetime
	from datetime import timedelta
	# import datetime
	year = request.GET.get('year', '')
	workweek = request.GET.get('week', '')

	# Display Mode (Desk top or Mobile)
	view = request.GET.get('view', '')

	if workweek=='' and year=='':
		# Use current week
		today= datetime.date.today()
		from_date = today -  timedelta(days=today.weekday())
		to_date = from_date +  timedelta(days=7)
		year = from_date.strftime('%Y')#-%m-%d %H:%M
		workweek = from_date.strftime('%W')
	else:
		# from isoweek import Week
		d = foo(int(year),int(workweek))
		from_date = d[0]
		to_date = d[1]
		print(d)
	# wk = from_date.isocalendar()[1]
	# ------------

	b = Voy.objects.filter(
		Q(etb__range=[from_date,to_date]),
		# Q(etd__range=[from_date,to_date]),
		terminal='B1',
		vessel__v_type='VESSEL',
		load_no__gt=0,
		draft=False).exclude(service__name__icontains='DIS').order_by('etb')


	a = Voy.objects.filter(
		Q(etb__range=[from_date,to_date]),
		# Q(etd__range=[from_date,to_date]),
		terminal__name__icontains ='A',
		vessel__v_type='VESSEL',
		load_no__gt=0,
		draft=False).exclude(
			service__name__icontains='DIS'
		).order_by('etb')

	# lastupdate = Voy.objects.filter(
	# 	Q(etb__range=[from_date,to_date]),
	# 	vessel__v_type='VESSEL',
	# 	draft=False).exclude(service__name__icontains='DIS').order_by('etb').aggregate(Max('modified_date'))

	c = Voy.objects.filter(
		Q(etb__range=[from_date,to_date]),
		Q(terminal='B1')|
		Q(terminal__name__icontains='A'),
		vessel__v_type='VESSEL',
		draft=False).exclude(service__name__icontains='DIS').order_by('-modified_date')

	lastupdate = c.first()
	# print ('Last update %s' % lastupdate)

	if view =='mobile':
		fname = 'bayplan/mobile_bayplan_index.html'
	else:
		fname = 'bayplan/bayplan_index.html'

	return render(request, fname, {'A':a,
						'B':b,
						'year':year,
						'week':workweek,
						'lastupdate':lastupdate})