from django.shortcuts import render

# Create your views here.

# from django.contrib.staticfiles.templatetags.staticfiles import static
from django.http import HttpResponse
import os.path
from django.conf import settings

from .models import ReportFile,Voy,cutoff,Service

from django.shortcuts import get_object_or_404
from django.views.generic import DetailView,CreateView,UpdateView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .forms import CutoffForm,ReturnStartForm

class VoyDetailView(DetailView):
	model = Voy

class CutOffDetailView(DetailView):
	model = cutoff

class CutOffUpdateView(LoginRequiredMixin,UpdateView):
	model = cutoff
	template_name = 'berth/cutoff_detail_update.html'
	form_class = CutoffForm

	def get_queryset(self):
		qs = super(CutOffUpdateView, self).get_queryset()
		return qs.all()

	def get_form_kwargs(self):
		kwargs = super(CutOffUpdateView,self).get_form_kwargs()
		# print(kwargs)
		return kwargs

class CutOffCreateView(LoginRequiredMixin,CreateView):
	# model = cutoff
	template_name = 'form.html'
	form_class = CutoffForm

	def form_valid(self,form):
		voy = get_object_or_404(Voy, slug=self.kwargs.get('slug'))
		form.instance.voy = voy
		obj = form.save(commit=False)
		return super(CutOffCreateView,self).form_valid(form)

	# def get_initial(self):
	# 	# print ('get_initial %s' % self.kwargs)
	# 	voy = get_object_or_404(Voy, slug=self.kwargs.get('slug'))
	# 	return {'voy':voy}

	def get_form_kwargs(self):
		kwargs = super(CutOffCreateView,self).get_form_kwargs()
		# kwargs['instance'] = Item.objects.filter(user=self.request.user).first()
		# print ('Kwarg %s' % self.request)
		return kwargs

	# # def get_queryset(self):
	# # 	return Item.objects.filter(user=self.request.user)
	def get_queryset(self):
		qs = super(CutOffUpdateView, self).get_queryset()
		return qs.filter(voy__vessel__v_type='VESSEL')

	def get_context_data(self,*args,**kwargs):
		context = super(CutOffCreateView,self).get_context_data(*args,**kwargs)
		context['title']='Add Cut-Off Datetime'
		# context['voy']= 'Add Cut-Off Datetime'
		return context

class CutOffDeleteView(LoginRequiredMixin,DeleteView):
	model = cutoff
	success_url = reverse_lazy('berth:cutoff-home')

	def get_object(self, queryset=None):
		obj = super(CutOffDeleteView, self).get_object()
		# print ('Delete %s' % obj)
		return obj

	def get_success_url(self):
	# Assuming there is a ForeignKey from Comment to Post in your model
		voy = self.object.voy 
		# print (voy)
		return reverse_lazy( 'berth:voy-detail', kwargs={'slug': voy.slug})

	# def get_form_kwargs(self):
	# 	kwargs = super(CutOffDeleteView,self).get_form_kwargs()
	# 	print('Kwargs %s' % kwargs)
	# 	return kwargs


# def xls_to_response(xls, fname):
#     response = HttpResponse(mimetype="application/ms-excel")
#     response['Content-Disposition'] = 'attachment; filename=%s' % fname
#     xls.save(response)
#     return response


# def index(request):
#     response = HttpResponse(mimetype="application/ms-excel")
#     response['Content-Disposition'] = 'attachment; filename=test.xlsm'
#     xls.save(response)
#     return response

def etb(request,vessel_code,voy):
	qs = Voy.objects.get(code=vessel_code,voy__contains=voy)
	if qs:
		return HttpResponse(qs.etb, content_type='text/plain; charset=utf8')
	else:
		return HttpResponse('', content_type='text/plain; charset=utf8')

# Added on April 26,2021 -- To provide ETD (departured time)
def etd(request,vessel_code,voy):
	try :

		qs = Voy.objects.get(code=vessel_code,voy__contains=voy)
		if qs:
			return HttpResponse(qs.etd, content_type='text/plain; charset=utf8')
		else:
			return HttpResponse('', content_type='text/plain; charset=utf8')
	except :
		return HttpResponse('', content_type='text/plain; charset=utf8')

def mobile_index(request):
	return HttpResponse(qs.etb, content_type='text/plain; charset=utf8')



def index(request):
	# return HttpResponse("Autoberth System", content_type='text/plain; charset=utf8')
	# reports = ReportFile.objects.all().order_by('-modified_date')
	return render(request, 'index.html', {})


def export(request):
	services = Service.objects.all()
	date_from = request.GET.get('from')
	date_to = request.GET.get('to')
	service = request.GET.get('service')
	qs =None
	if date_to != None and date_from != None and service != None :
		qs= Voy.objects.filter(service__name=service ,
			eta__range=[date_from,date_to]).order_by('eta')
		
	return render(request, 'berth/export.html', {'services':services,
		'qs':qs})



def pdf_view(request):
	vFileName ='test.pdf'
	full_path = os.path.join(settings.STATIC_ROOT, vFileName) #static(vFileName)
	with open(full_path, 'rb') as pdf:
		response = HttpResponse(pdf.read(),content_type='application/pdf')
		response['Content-Disposition'] = 'filename=some_file.pdf'
	return response
	# pdf, response = pdf_response('filename_without_extension')
	# # ... more code
	# pdf.generate()
	# return HttpResponse(full_path)


# Add by Chutchai on Nov 23,2017
# to Show Auto Cut-off datetime
def foo(year, week):
	# from datetime import date, timedelta
	# d = date(year,1,1)
	# dlt = timedelta(days = ((week-1)*7)-1)
	# return d + dlt ,  d + dlt + timedelta(days=8)
	import datetime
	from datetime import timedelta
	d = '%s-W%s' % (year,week)
	from_date = datetime.datetime.strptime(d + '-1', "%Y-W%W-%w")
	to_date = from_date + timedelta(days=7)
	return from_date,to_date
	# Comment by Chutchai on Jan 16,2019
	# To fix cut-off workweek report show wrong date range
	# dlt = timedelta(days = ((week-1)*7))
	# return d + dlt ,  d + dlt + timedelta(days=7)

def cutoff(request):
	from django.db.models import Q
	from django.db.models import Max
	# from datetime import datetime
	import datetime
	from datetime import timedelta
	# import datetimequit
	year = request.GET.get('year', '')
	workweek = request.GET.get('week', '')
	import pytz
	from datetime import datetime
	tz = pytz.timezone('Asia/Bangkok')
	today = datetime.now(tz=tz).replace(tzinfo=None) #remove aware timezone

	if workweek=='' and year=='':
		# Use current week
		# today= datetime.date.today()
		

		from_date = today -  timedelta(days=today.weekday())
		to_date = from_date +  timedelta(days=8)

		# Edit on Jan 9,2021 to Fix wrong Workweek
		to_date = from_date +  timedelta(days=7)
		
		# Edit by Chutchai on Jan 2,2019
		# To fix WorkWeek problem
		# year = from_date.strftime('%Y')#-%m-%d %H:%M
		year = to_date.strftime('%Y')#-%m-%d %H:%M
		# workweek = from_date.strftime('%W')
		# workweek = datetime.date(from_date.year, from_date.month, from_date.day).isocalendar()[1]
		workweek = today.isocalendar()[1]
		print ('Current from: %s to %s' % (from_date,to_date))
	else:
		# from isoweek import Week
		# print (year,workweek)
		d = foo(int(year),int(workweek))
		from_date = d[0]
		to_date = d[1]
		print ('Week assign from: %s to %s' % (from_date,to_date))
	# wk = from_date.isocalendar()[1]
	# ------------

	# b = Voy.objects.filter(
	# 	Q(etb__range=[from_date,to_date]),
	# 	# Q(etd__range=[from_date,to_date]),
	# 	terminal='B1',
	# 	vessel__v_type='VESSEL',
	# 	draft=False).exclude(service__name__icontains='DIS').order_by('etb')

	b = Voy.objects.filter(
		Q(etb__range=[from_date,to_date]),
		# Q(etd__range=[from_date,to_date]),
		terminal='B1',
		vessel__v_type='VESSEL',
		draft=False).exclude(load_no=0).order_by('etb')

	# .values('vessel','code','voy','service','etd','etb','slug')
	# b_obj_list =list(b)
	# print (b_obj_list)


	# a = Voy.objects.filter(
	# 	Q(etb__range=[from_date,to_date]),
	# 	# Q(etd__range=[from_date,to_date]),
	# 	terminal__name__icontains ='A',
	# 	vessel__v_type='VESSEL',
	# 	draft=False).exclude(
	# 		service__name__icontains='DIS'
	# 	).order_by('etb')
	a = Voy.objects.filter(
		Q(etb__range=[from_date,to_date]),
		terminal__name__icontains ='A',
		vessel__v_type='VESSEL',
		draft=False).exclude(load_no=0).order_by('etb')

	# .values('vessel','code','voy','service','etd','etb','slug')
	# a_obj_list =list(a)
	# Comment on March 22,2018
	# To import performance
	# c = Voy.objects.filter(
	# 	Q(etb__range=[from_date,to_date]),
	# 	Q(terminal='B1')|
	# 	Q(terminal__name__icontains='A'),
	# 	vessel__v_type='VESSEL',
	# 	draft=False).exclude(service__name__icontains='DIS').order_by('-modified_date').values('vessel','code','voy','modified_date')
	c = Voy.objects.filter(
		Q(etb__range=[from_date,to_date]),
		vessel__v_type='VESSEL',
		draft=False).exclude(
			terminal='B2',load_no=0).order_by('-modified_date').values(
				'vessel','code','voy','modified_date')

	c_obj_list =list(c)
	lastupdate = c_obj_list[0]
	# print(lastupdate['modified_date'])

	print ('Year %s , Week %s' % (year,workweek))

	return render(request, 'cutoff.html', {'A':a,
						'B':b,
						'year':year,
						'week':workweek,
						'lastupdate':lastupdate})




def truckWindow(request):
	from django.db.models import Q
	from django.db.models import Max
	# from datetime import datetime
	import datetime
	from datetime import timedelta
	# import datetimequit
	year = request.GET.get('year', '')
	workweek = request.GET.get('week', '')
	import pytz
	from datetime import datetime
	tz = pytz.timezone('Asia/Bangkok')
	today = datetime.now(tz=tz).replace(tzinfo=None) #remove aware timezone

	if workweek=='' and year=='':
		from_date = today -  timedelta(days=today.weekday())
		to_date = from_date +  timedelta(days=8)
		# Edit on Jan 9,2021 to Fix wrong Workweek
		to_date = from_date +  timedelta(days=14)
		year = to_date.strftime('%Y')#-%m-%d %H:%M
		workweek = today.isocalendar()[1]
		print ('Current from: %s to %s' % (from_date,to_date))
	else:
		d = foo(int(year),int(workweek))
		from_date = d[0]
		to_date = d[1]
		print ('Week assign from: %s to %s' % (from_date,to_date))

	voys = Voy.objects.filter(
		Q(etb__range=[from_date,to_date]),
		vessel__v_type='VESSEL',
		draft=False,load_no__gt=0).exclude(
			Q(terminal='B2')|Q(load_no=0)).order_by('etb')

	return render(request, 'truckwindow.html', {'object_list':voys})

from django.contrib.auth.mixins import PermissionRequiredMixin
class ReturnStartUpdateView(PermissionRequiredMixin,UpdateView):
	permission_required = 'berth.change_return_date'
	model = Voy
	template_name = 'berth/return_start_update.html'
	form_class = ReturnStartForm
	success_url = reverse_lazy('berth:truck-window')