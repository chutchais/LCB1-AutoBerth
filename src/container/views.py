from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.views import View
from django.views.generic import TemplateView,ListView,DetailView,CreateView,UpdateView
from django.db.models import Q,F
import django_excel as excel
import xlrd
import re
from django.db.models import Count,Sum,Value, When,Case,IntegerField,CharField
from django.urls import reverse_lazy
# from django.core.urlresolvers import reverse
from django.urls import reverse
from django.shortcuts import redirect
from django.conf import settings
from django.utils.text import slugify

from .models import Container,DischargePort
from .forms import ContainerForm
from  bayplan.models import BayPlanFile



under_deck = ['18','16','14','12','10','08','06','04','02']
# over_deck =['94','92','90','88','86','84','82','80']
over_deck =['94','92','90','88','86','84','82','80','78','76','74','72']

tier1 =['18','16','14','12','10','08','06','04','02','00','01','03','05','07','09','11','13','15','17']
tier2 =['18','16','14','12','10','08','06','04','02','00','01','03','05','07','09','11','13','15','17']



class ContainerDetailView(LoginRequiredMixin,DetailView):
	model = Container
	# def get_queryset(self):
	# 	slug = self.kwargs['slug']
	# 	return Container.objects.filter(slug=slug)

class MobileContainerUpdateView(LoginRequiredMixin,UpdateView):
	model = Container
	template_name = 'container/mobile_container_detail_update.html'
	
	form_class = ContainerForm

	def get_context_data(self, **kwargs):
		context = super(ContainerUpdateView, self).get_context_data(**kwargs)
		context['bay'] = self.request.GET.get('bay')
		# print (self.object.bay)
		# get Row
		row = self.object.stowage[-2:]
		if  row in over_deck :
			context['deck'] = over_deck
		else :
			context['deck'] = under_deck

		context['tier'] = tier1
		context['pos'] = self.request.GET.get('pos')
		# print (self.object.bay)
		return context

	def get_success_url(self,*args, **kwargs):
		# print('Slug %s' % self.object.bayplanfile.slug)
		mode = self.request.GET.get('mode')
		view = self.request.GET.get('view')
		pos  = self.request.GET.get('pos')
		# print(mode)
		slug =self.object.bayplanfile.slug
		bay = self.object.bay
		# print ('Bay %s'% bay)
		if mode=='search':
			query = self.request.GET.get('q')
			url = reverse('container:bay',kwargs={'slug':slug})
			url = '%s?q=%s&view=%s&pos=%s' % (url , query,view,pos)
		else :
			url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
			url = '%s?q=%s&view=%s&pos=%s' % (url , self.object.container,view,pos)
		
		return url

class ContainerUpdateView(LoginRequiredMixin,UpdateView):
	model = Container
	template_name = 'container/mobile_container_detail_update.html'
	
	form_class = ContainerForm
	# success_url = reverse_lazy('container:detail',kwargs={})

	# Comment on Feb 2,2018 -- To improve Save speed
	# def get_queryset(self):
	# 	print ('Stowage Update -- Get_Queryset')
	# 	qs = super(ContainerUpdateView, self).get_queryset()
	# 	return qs.all()

	# Comment on Feb 2,2018 -- To improve Save speed
	# def get_form_kwargs(self):
	# 	kwargs = super(ContainerUpdateView,self).get_form_kwargs()
	# 	# kwargs['stowage'] = self.object.stowage
	# 	print(self.request.GET.get('view'))
	# 	return kwargs

	def get_context_data(self, **kwargs):
		context = super(ContainerUpdateView, self).get_context_data(**kwargs)
		bay = self.request.GET.get('bay')
		context['bay'] = bay
		# print (self.object.bay)
		# get Row
		row = self.object.stowage[-2:]
		if  row in over_deck :
			context['deck'] = over_deck
		else :
			context['deck'] = under_deck

		context['tier'] = tier1
		context['pos'] = self.request.GET.get('pos')

		c_master = Container.objects.filter(bayplanfile__slug=self.object.bayplanfile.slug,original_bay=bay)
		c_master_slot_list = c_master.values_list('original_stowage', flat=True)
		
		# To show current Weight of bay
		c_current = Container.objects.filter(bayplanfile__slug=self.object.bayplanfile.slug,bay=bay)
		c_current_slot_list = c_current.values_list('stowage','weight')
		# x=next(y for y in c_current_slot_list if y[0]=='010102')
		

		context['master_plan'] = c_master_slot_list
		context['current_plan'] = c_current_slot_list

		# print (self.object.bay)
		return context
		# if 'bay' in self.kwargs:
			

		    # context['object'] = get_object_or_404(MyObject, slug=self.kwargs['slug'])
		#     context['objects'] = get_objects_by_user(self.request.user)
		

	def get_success_url(self,*args, **kwargs):
		# print('Slug %s' % self.object.bayplanfile.slug)
		mode = self.request.GET.get('mode')
		view = self.request.GET.get('view')
		pos  = self.request.GET.get('pos')
		# print(mode)
		slug =self.object.bayplanfile.slug
		bay = self.object.bay
		# print ('Bay %s'% bay)
		if mode=='search':
			query = self.request.GET.get('q')
			url = reverse('container:bay',kwargs={'slug':slug})
			url = '%s?q=%s&view=%s&pos=%s' % (url , query,view,pos)
		else :
			url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
			url = '%s?q=%s&view=%s&pos=%s' % (url , self.object.container,view,pos)
		
		return url
		# reverse_lazy('container:detail',kwargs={'slug':slug,'bay':bay},query={'q':self.object.container})
		# return reverse(url)

	# Comment on Feb 2,2018 -- To improve Save speed
	# def form_valid(self,form,*args, **kwargs):
	# 	# action = request.GET.get('action')
	# 	# print ('Valid form %s' % action)
	# 	obj = form.save(commit=False)
	# 	# obj.user = self.request.user
	# 	return super(ContainerUpdateView,self).form_valid(form)


class ContainerListView(LoginRequiredMixin,ListView):
	# template_name = 'restaurants/restaurants_list.html' # default name =restaurantlocation_list.html
	model = Container
	# def get_queryset(self):
	# 	slug = self.kwargs['slug']
	# 	return Container.objects.filter(bayplanfile__slug = slug)

def ContainerRestore(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	c = Container.objects.get(slug=slug)
	c.stowage = c.original_stowage
	c.bay = c.original_bay
	c.ready_to_load = False
	c.save()


	slug = c.bayplanfile.slug
	bay = c.bay

	mode = request.GET.get('mode')
	view = request.GET.get('view')
	pos = request.GET.get('pos')
	if mode=='search':
		query = request.GET.get('q')
		url = reverse('container:bay',kwargs={'slug':slug})
		url = '%s?q=%s&view=%s&pos=%s' % (url , query,view,pos)
	else:
		url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
		url = '%s?q=%s&view=%s&pos=%s' % (url , c.container,view,pos)

	return HttpResponseRedirect(url)

def ContainerMove(request,slug,slot):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	# print (slug,slot)
	c = Container.objects.get(slug=slug)
	c.stowage = slot
	c.ready_to_load = True
	c.save()


	slug = c.bayplanfile.slug
	bay = c.bay

	mode = request.GET.get('mode')
	view = request.GET.get('view')
	pos = request.GET.get('pos')
	if mode=='search':
		query = request.GET.get('q')
		url = reverse('container:bay',kwargs={'slug':slug})
		url = '%s?q=%s&view=%&pos=%s' % (url , query,view,pos)
	else:
		url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
		url = '%s?q=%s&view=%s&pos=%s' % (url , c.container,view,pos)

	return HttpResponseRedirect(url)


def BayRestore(request,slug,bay):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))


	container_list = Container.objects.filter(bayplanfile__slug=slug,bay=bay)
	for  c in container_list:
		if c.stowage != c.original_stowage:
			c.stowage = c.original_stowage
			c.bay = c.original_bay
			c.save()


	# slug = c.bayplanfile.slug
	# bay = c.bay
	url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
	# print (url)
	# mode = request.GET.get('mode')
	# if mode=='search':
	# 	query = request.GET.get('q')
	# 	url = reverse('container:bay',kwargs={'slug':slug})
	# 	url = '%s?q=%s' % (url , query)
	# else:
	# 	url = reverse('container:detail',kwargs={'slug':slug,'bay':bay})
	# 	# url = '%s?q=%s' % (url , c.container)

	return HttpResponseRedirect(url)

def FileReady(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	action = request.GET.get('action')
	container_list = Container.objects.filter(bayplanfile__slug=slug)
	container_list.update(ready_to_load=True if action=='set' else False)
	# for  c in container_list:
	# 	# if c.stowage != c.original_stowage:
	# 	c.ready_to_load = True if action=='set' else False
	# 	c.save()
	url = reverse('container:bay',kwargs={'slug':slug})
	return HttpResponseRedirect(url)

def BayReady(request,slug,bay):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	action = request.GET.get('action')
	container_list = Container.objects.filter(bayplanfile__slug=slug,bay=bay)
	container_list.update(ready_to_load=True if action=='set' else False)
	# for  c in container_list:
	# 	# if c.stowage != c.original_stowage:
	# 	c.ready_to_load = True if action=='set' else False
	# 	c.save()
	url = reverse('container:bay',kwargs={'slug':slug})
	return HttpResponseRedirect(url)


def BayReport(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
	# print(slug)
	query = request.GET.get('q')
	bayfile =BayPlanFile.objects.get(slug=slug)
	c = Container.objects.filter(bayplanfile__slug=slug)

	view = request.GET.get('view','')
	if view=='mobile':
		fname='container/mobile_bay.html'
	else:
		fname='container/bay.html'
	
	if not query :
		# Show Overall view
		b = c.values('bay').annotate(
			number=Count('container'),
			move=Sum(Case(When( stowage = F('original_stowage'),then=Value(0)),default=Value(1),output_field=IntegerField())),
			ready=Sum(Case(When( ready_to_load = True,then=Value(1)),default=Value(0),output_field=IntegerField()))
			)
		dup = c.values('stowage','bay').annotate(number=Count('container')).exclude(number=1)
		# print (Container.objects.filter(bayplanfile__slug=slug,stowage='270708'))

		return render(
			request,
			fname,
			{
			'bays': b,
			'bayfile':bayfile,
			'dups':dup}
			)
	else:
		#show Search result
		# print ('Hello World')
		qs = c.filter(container__icontains=query).order_by('container')
		return render(
			request,
			fname,
			{
			'bays': None,
			'bayfile':bayfile,
			'dups':None,
			'container_list':qs}
			)


def BayDetail(request,slug,bay):
	# print(slug,bay)
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	query = request.GET.get('q',None)
	mode = request.GET.get('mode','container')
	# print ('Mode:%s' % mode)

	view = request.GET.get('view','')
	pos = request.GET.get('pos','')

	# bayfile =BayPlanFile.objects.get(slug=slug)
	if view == 'mobile':
		c = Container.objects.filter(bayplanfile__slug=slug,bay=bay,ready_to_load=True)
	else:
		c = Container.objects.filter(bayplanfile__slug=slug,bay=bay)
	

	if c :
		c_slot_list = c.values_list('stowage', flat=True)
		c_list = list(c)
	else:
		c_slot_list=[]
		c_list=[]

	c_master = Container.objects.filter(bayplanfile__slug=slug,original_bay=bay)
	c_master_slot_list = c_master.values_list('original_stowage', flat=True)
	c_master_list = list(c_master)



	# Find changes slot
	has_changes = False
	b = c.exclude(stowage = F('original_stowage')).count()
	if b > 0 :
		has_changes = True
	# -----------------


	tier = tier1 #Default

	# Fit tier and Over/Under Deck(Row)
	# Tier = row
	# Stack = col
	# Over Deck = Tier > 70
	# Under Deck = Tier < 50
	has_on_deck = False
	has_under_deck = False
	tier_test =[]
	for obj in c_master:
		row = obj.stowage[-2:]
		if int(row) > 70:
			has_on_deck = True
		if int(row) < 30:
			has_under_deck = True

		col = obj.stowage[-4:4]
		if not col in tier_test:
			tier_test.append(col)
	
	# print ('Request by PC : %s' % request.user_agent.is_pc)

	if view =='mobile':
		fname='container/mobile_bay_detail.html'
		# tier =[x for x in tier if x in tier_test]
	else:
		fname='container/bay_detail.html'

	# Show Under Deck First ,if exist
	
	# print (pos)
	if pos == '':
		if has_under_deck :
			deck = under_deck
			deck_pos = 'UD'
			pos='UD'
		else :
			deck = over_deck
			deck_pos = 'OD'
			pos='OD'
	else:
		# print(pos)
		deck_pos = pos
		deck = under_deck if pos == 'UD' else over_deck

	


	return render(
		request,
		fname,
		{
		'container_list': c,
		'container_slot_list': c_slot_list,
		'container_obj_list': c_list,
		'has_change' :has_changes,
		'slug':slug,
		'bay': bay,
		'deck' : deck,
		'pos' : deck_pos,
		'master_plan':c_master,
		'master_slot_list': c_master_slot_list,
		'master_obj_list': c_master_list,
		'under_deck': under_deck,
		'over_deck':over_deck,
		'tier': tier,
		'full_tier': tier1,
		'q':query,
		'mode': True if mode=='container' else False ,
		'has_on_deck': has_on_deck,
		'has_under_deck':has_under_deck}
		)

# filehandle.read()
def FileProcess(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	bayfile =BayPlanFile.objects.get(slug=slug)
	book = xlrd.open_workbook(file_contents=bayfile.filename.read())
	xl_sheet = book.sheet_by_index(0)
	print ('Sheet name: %s' % xl_sheet.name)
	print ('Total row %s' % xl_sheet.nrows )
	print ('Total col %s' % xl_sheet.ncols)

	regex='^[A-Z]{4}[0-9]{7}$'
	item_count =0
	new_count = 0
	Container.objects.filter(bayplanfile=bayfile).delete()
	container_list = []
	non_stowage_list = []

	voy_number = bayfile.voy.voy

	for row_index in range(1, xl_sheet.nrows):
		load_port	= xl_sheet.cell(row_index, 10).value.__str__().strip()
		if load_port !='THLCH':
			continue


		vContainer = xl_sheet.cell(row_index, 1).value.__str__().strip()
		if re.match(regex,vContainer):
			item_count = item_count+1
			# Reading all value
			iso 		= xl_sheet.cell(row_index, 2).value.__str__().strip()
			full 		= xl_sheet.cell(row_index, 3).value.__str__().strip()
			partner		= xl_sheet.cell(row_index, 5).value.__str__().strip()
			weight		= xl_sheet.cell(row_index, 6).value.__str__().strip().replace('.0','')
			load_port	= xl_sheet.cell(row_index, 10).value.__str__().strip()
			dis_port	= xl_sheet.cell(row_index, 11).value.__str__().strip()
			delivery_port= xl_sheet.cell(row_index, 12).value.__str__().strip()
			desc        = xl_sheet.cell(row_index, 17).value.__str__().strip()
			imdg        = xl_sheet.cell(row_index, 18).value.__str__().strip().replace('.0','')
			un_no       = xl_sheet.cell(row_index, 19).value.__str__().strip().replace('.0','')
			stowage		= xl_sheet.cell(row_index, 26).value.__str__().strip().replace('.0','')

			
			# Add by Chutchai on June 24
			# To check empty stowage field
			# print ('Stowage %s - %s ' %  (vContainer,stowage))
			if stowage == '' or stowage == None :
				# print ('Found empty stowage %s ' %  vContainer)
				non_stowage_list.append(vContainer)
				continue
				# return "Error"

			# --------------------------

			if load_port !='THLCH':
				# print ('Not load at LCB %s' % load_port )
				continue

			if len(stowage)==5:
				stowage = '0%s'% stowage
				# print (stowage)
			# Get Disch Port Object
			disport_obj,created = DischargePort.objects.get_or_create(name=dis_port)
			container_slug = slugify("%s-%s-%s" %(vContainer,item_count, voy_number))
			c = Container(bayplanfile=bayfile,item_no=item_count,
								container=vContainer,iso_code=iso,full=True if full=='Full' else False,
								slug=container_slug,
								partner=partner,weight=weight,
								load_port=load_port,dis_port=disport_obj,deliverly_port=delivery_port,
								good_desc=desc,
								stowage=stowage,bay=stowage[:1] if len(stowage)==5 else stowage[:2],
								original_stowage=stowage,original_bay=stowage[:1] if len(stowage)==5 else stowage[:2],
								imdg=imdg,un_no=un_no)


			container_list.append(c)

	# print (non_stowage_list)
	if len(non_stowage_list)>0:
		fname ='container/container_empty_stowage.html'
		print ('Found %s containers are empty stowage' % len(non_stowage_list))
		return render(
				request,
				fname,
				{
				'object_list': non_stowage_list,
				'number': len(non_stowage_list),
				'slug' : bayfile.voy.slug 
				}
			)

	Container.objects.bulk_create(container_list)
			# c = Container.objects.create(bayplanfile=bayfile,item_no=item_count,
			# 					container=vContainer,iso_code=iso,full=True if full=='Full' else False,
			# 					partner=partner,weight=weight,
			# 					load_port=load_port,dis_port=disport_obj,deliverly_port=delivery_port,
			# 					good_desc=desc,
			# 					stowage=stowage,bay=stowage[:1] if len(stowage)==5 else stowage[:2],
			# 					original_stowage=stowage,original_bay=stowage[:1] if len(stowage)==5 else stowage[:2] )
			# =============
	return redirect(reverse_lazy( 'container:bay', kwargs={'slug': slug}))


def FileUpdate(request,slug):
	if not request.user.is_authenticated:
		return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

	bayfile =BayPlanFile.objects.get(slug=slug)
	book = xlrd.open_workbook(file_contents=bayfile.updated_filename.read())
	xl_sheet = book.sheet_by_index(0)
	print ('Sheet name: %s' % xl_sheet.name)
	print ('Total row %s' % xl_sheet.nrows )
	print ('Total col %s' % xl_sheet.ncols)

	regex='^[A-Z]{4}[0-9]{7}$'
	item_count =0
	new_count = 0

	# Find Not Ready Bay.
	bay_list_tmp = bayfile.container_set.filter(ready_to_load=False).values('bay').annotate(
			total=Count('container')
			).values_list('bay', flat=True)
	# m_list = m.values_list('machine_name', flat=True)
	bay_list = []
	for i in bay_list_tmp:
		bay_list.append(i)

	# print(bay_list)
	Container.objects.filter(bayplanfile=bayfile , bay__in=bay_list).delete()
	container_list = []

	for row_index in range(1, xl_sheet.nrows):
		load_port	= xl_sheet.cell(row_index, 10).value.__str__().strip()
		if load_port !='THLCH':
			continue

		vContainer = xl_sheet.cell(row_index, 1).value.__str__().strip()
		if re.match(regex,vContainer):
			item_count = item_count+1
			# Reading all value
			iso 		= xl_sheet.cell(row_index, 2).value.__str__().strip()
			full 		= xl_sheet.cell(row_index, 3).value.__str__().strip()
			partner		= xl_sheet.cell(row_index, 5).value.__str__().strip()
			weight		= xl_sheet.cell(row_index, 6).value.__str__().strip().replace('.0','')
			load_port	= xl_sheet.cell(row_index, 10).value.__str__().strip()
			dis_port	= xl_sheet.cell(row_index, 11).value.__str__().strip()
			delivery_port= xl_sheet.cell(row_index, 12).value.__str__().strip()
			desc        = xl_sheet.cell(row_index, 17).value.__str__().strip()
			imdg        = xl_sheet.cell(row_index, 18).value.__str__().strip().replace('.0','')
			un_no       = xl_sheet.cell(row_index, 19).value.__str__().strip().replace('.0','')
			stowage		= xl_sheet.cell(row_index, 26).value.__str__().strip().replace('.0','')

			if load_port !='THLCH':
				print ('Not load at LCB %s' % load_port )
				continue

			if len(stowage)==5:
				stowage = '0%s'% stowage
				print (stowage)

			if not stowage[:2] in bay_list:
				# print('%s is no need to update' % stowage[:2])
				continue
			# Get Disch Port Object
			disport_obj,created = DischargePort.objects.get_or_create(name=dis_port)

			# c = Container.objects.create(bayplanfile=bayfile,item_no=item_count,
			# 					container=vContainer,iso_code=iso,full=True if full=='Full' else False,
			# 					partner=partner,weight=weight,
			# 					load_port=load_port,dis_port=disport_obj,deliverly_port=delivery_port,
			# 					good_desc=desc,
			# 					stowage=stowage,bay=stowage[:1] if len(stowage)==5 else stowage[:2],
			# 					original_stowage=stowage,original_bay=stowage[:1] if len(stowage)==5 else stowage[:2] )
			container_slug = slugify("%s-%s" %(vContainer, item_count))
			c = Container(bayplanfile=bayfile,item_no=item_count,
								container=vContainer,iso_code=iso,full=True if full=='Full' else False,
								slug=container_slug,
								partner=partner,weight=weight,
								load_port=load_port,dis_port=disport_obj,deliverly_port=delivery_port,
								good_desc=desc,
								stowage=stowage,bay=stowage[:1] if len(stowage)==5 else stowage[:2],
								original_stowage=stowage,original_bay=stowage[:1] if len(stowage)==5 else stowage[:2] ,
								imdg=imdg,un_no=un_no)

			container_list.append(c)
			# =============
	Container.objects.bulk_create(container_list)

	# Delete Updated-filename
	bayfile.updated_filename = None
	bayfile.save()

	return redirect(reverse_lazy( 'container:bay', kwargs={'slug': slug}))
