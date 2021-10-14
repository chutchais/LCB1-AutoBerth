from django.db import models
from colorfield.fields import ColorField
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.core.exceptions import ValidationError

from datetime import datetime, timedelta

from django.urls import reverse

import json
from django.db.models.signals import post_save,pre_save,pre_delete
from django_q.tasks import async_task

# Create your models here.
ACTIVE='A'
DEACTIVE='D'
STATUS_CHOICES = (
		(ACTIVE, 'Active'),
		(DEACTIVE, 'Deactive'),
	)


class Terminal(models.Model):
	name = models.CharField(max_length=50,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	start_range = models.CharField(verbose_name ='Excel start range',max_length=2,blank=True, null=True)
	stop_range = models.CharField(verbose_name ='Excel stop range',max_length=2,blank=True, null=True)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	# user = models.ForeignKey('auth.User',blank=True,null=True)
	user = models.ForeignKey('auth.User',blank=True,null=True,on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.name


class Service(models.Model):
	name = models.CharField(max_length=50,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	color = ColorField(default='#CCFFFF')
	move_performa =  models.IntegerField(verbose_name ='Move Performa',default=0)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	# user = models.ForeignKey('auth.User',blank=True,null=True)
	user = models.ForeignKey('auth.User',blank=True,null=True,on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.name

class Vessel(models.Model):
	V = 'VESSEL'
	B ='BARGE'
	N = 'NOTICE'
	VESSEL_TYPE_CHOICES = (
		(V, 'Vessel'),
		(B, 'Barge'),
		(N, 'Notice'),
	)
	name = models.CharField(max_length=50,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	lov = models.IntegerField(verbose_name ='Lenght of Vessel',default=100)
	imo = models.CharField(verbose_name ='IMO number',max_length=20,blank=True, null=True)
	v_type = models.CharField(verbose_name ='Vessel Type',max_length=10,choices=VESSEL_TYPE_CHOICES,default=V)
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	# user = models.ForeignKey('auth.User',blank=True,null=True)
	user = models.ForeignKey('auth.User',blank=True,null=True,on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.name

class Voy(models.Model):
	R = 'R'
	L ='L'
	T = 'T'
	B = 'B'
	TEXT_POS_CHOICES = (
		(R, 'Right'),
		(L, 'Left'),
		(T, 'Top'),
		(B, 'Buttom'),
	)
	voy = models.CharField(max_length=50 )#,primary_key=True
	slug = models.SlugField(unique=True,blank=True, null=True)
	code = models.CharField(max_length=20,blank=True, null=True)
	# vessel = models.ForeignKey('Vessel', related_name='plans')
	# service = models.ForeignKey('Service', related_name='plans')
	# terminal = models.ForeignKey('Terminal', related_name='plans')
	vessel = models.ForeignKey('Vessel', related_name='plans',on_delete=models.CASCADE)
	service = models.ForeignKey('Service', related_name='plans',on_delete=models.CASCADE)
	terminal = models.ForeignKey('Terminal', related_name='plans',on_delete=models.CASCADE)
	start_pos = models.IntegerField(verbose_name ='Start Position',default=50)
	performa_in =  models.DateTimeField(blank=True, null=True)
	performa_out =  models.DateTimeField(blank=True, null=True)
	move_performa =  models.IntegerField(verbose_name ='Move Performa',default=0)
	move_confirm = models.BooleanField(verbose_name ='Move Confirm',default=False)
	eta =  models.DateTimeField(verbose_name ='ETA',blank=True, null=True)
	etb =  models.DateTimeField(verbose_name ='ETB',blank=True, null=True)
	etd =  models.DateTimeField(verbose_name ='ETD',blank=True, null=True)
	qc = models.CharField(verbose_name ='Q',max_length=20,blank=True, null=True)
	dis_no =  models.IntegerField(verbose_name ='Discharge',default=0)
	load_no =  models.IntegerField(verbose_name ='Loading',default=0)
	est_teu = models.IntegerField(verbose_name ='Est TEU',default=0)
	vsl_oper = models.CharField(verbose_name ='Vsl Operator',max_length=20,blank=True, null=True)
	arrival_draft = models.CharField(verbose_name ='Arrival draft',max_length=50,blank=True, null=True,default=0)
	departure_draft = models.CharField(verbose_name ='Departure draft',max_length=50,blank=True, null=True,default=0)
	remark = models.TextField(max_length=255,blank=True, null=True)
	draft = models.BooleanField(verbose_name ='Saved as Draft',default=False)
	text_pos = models.CharField(verbose_name ="Text position for Barge",max_length=1,choices=TEXT_POS_CHOICES,default=R)
	next_date = models.IntegerField(verbose_name ='Next arrive date',default=14)
	imp_release_date = models.DateTimeField(verbose_name ='Import Release Date',help_text='',blank=True, null=True)
	export_cutoff_date = models.DateTimeField(verbose_name ='Export Cutoff Date',blank=True, null=True)
	inverse = models.BooleanField(verbose_name ='Inverse 180',default=False)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)

	def __str__(self):
		return ('%s of %s' % (self.voy,self.vessel))

	def get_absolute_url(self):
		return reverse('berth:voy-detail', kwargs={'slug': self.slug})

	def has_cutoff(self):
		return True if self.cutoff_set.count()>0 else False

	def clean(self):
		if self.etd <= self.etb :
			raise ValidationError('ETD must be bigger than ETB')

		# if self.imp_release_date != None :
		# 	if self.imp_release_date <= self.etb :
		# 		raise ValidationError('Import Release Date must be after ETB')

		# if self.export_cutoff_date != None :
		# 	if self.export_cutoff_date >= self.etb :
		# 		raise ValidationError('Export Cutoff Date must be before ETB')

	def save(self, *args, **kwargs):
		teu_factor = 1.43
		if self.dis_no != 0 :
			teu_dis = self.dis_no * teu_factor
		else:
			teu_dis = 0

		if self.load_no != 0 :
			teu_load = self.load_no * teu_factor
		else :
			teu_load = 0
		self.est_teu = teu_dis + teu_load

		# if self.imp_release_date == None  :
		# 	self.imp_release_date = self.etb + timedelta(hours=24)
		delta = self.etd - self.etb
		hours = divmod(delta.total_seconds(), 3600)[0]
		print ('Port stay %s' % hours)
		if hours >= 12:
			self.imp_release_date = self.etb + timedelta(hours=12)
		else:
			self.imp_release_date = self.etd

		if self.export_cutoff_date == None :
			self.export_cutoff_date = self.etb - timedelta(hours=12)



		super(Voy, self).save(*args, **kwargs) # Call the "real" save() method.
	
	@property
	def json(self):
		import json
		import datetime, pytz
		tz = pytz.timezone('Asia/Bangkok')
		updated_tz = datetime.datetime.now(tz=tz)
		# json_dict =  {
		# 		'name' : self.name,
		# 		'resource_name':self.resource_name,
		# 		'grand_total':float(self.grand_total),
		# 		'charge':float(self.charge),
		# 		'vat': float(self.charge )* float(self.vat_rate)/100,
		# 		'wht':float(self.charge) * float(self.wht_rate)/100,
		# 		'iswht':self.wht,
		# 		'terminal':self.terminal,
		# 		'qrid': self.qrid,
		# 		'ref': self.ref,
		# 		'paid': self.paid,
		# 		'updated':updated_tz.strftime('%d-%m-%Y %H:%M:%S')
		# 	}
		json_dict = {
				'service': self.service.name,
				'vessel': self.vessel.name,
				'code': self.code,
				'voy': self.voy,
				'performa_in': self.performa_in.strftime('%Y-%m-%dT%H:%M:%S') ,#'2021-06-12T21:00:00',
				'performa_out': self.performa_out.strftime('%Y-%m-%dT%H:%M:%S') ,#'2021-06-15T16:00:00',
				'eta': self.eta.strftime('%Y-%m-%dT%H:%M:%S') ,#'2021-06-15T00:01:00',
				'etb': self.etb.strftime('%Y-%m-%dT%H:%M:%S') ,#'2021-06-15T01:00:00',
				'etd': self.etd.strftime('%Y-%m-%dT%H:%M:%S') ,#'2021-06-16T04:00:00',
				'lov': self.vessel.lov,
				'dis_no': self.dis_no,
				'load_no': self.load_no,
				'est_teu': self.est_teu,
				'terminal': self.terminal.name,
				'start_pos': self.start_pos,
				'vessel_type': self.vessel.v_type,
				'color': self.service.color,
				'remark': self.remark,
				'vsl_oper': self.vsl_oper,
				'arrival_draft': self.arrival_draft,
				'departure_draft': self.departure_draft,
				'slug': self.slug,
				'draft': self.draft,
				'startCol': self.terminal.start_range,
				'stopCol': self.terminal.stop_range,
				'move_performa':self.move_performa,
				'move_confirm':self.move_confirm,
				'text_pos':self.text_pos,
				'qc':self.qc,
				'inverse':self.inverse
			}
		return json.dumps(json_dict)
	# class Meta:
	# 	unique_together = ('voy', 'vessel',)

def post_save_voy_receiver(sender, instance,created, *args, **kwargs):
	async_task("berth.services.save_voy_to_redis",instance)
	# print (f'{"New " if created else "Modify "} Job : {instance} ,save to redis successful.')

post_save.connect(post_save_voy_receiver, sender=Voy)

# Handle Slug of Vessel

def create_vessel_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	# if new_slug is not None:
	# 	slug = new_slug
	# qs = Vessel.objects.filter(slug=slug).order_by("-id")
	# exists = qs.exists()
	# if exists:
	# 	new_slug = "%s-%s" %(slug, qs.first().lov)
	# 	return create_vessel_slug(instance, new_slug=new_slug)
	return slug


def pre_save_vessel_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_vessel_slug(instance)

pre_save.connect(pre_save_vessel_receiver, sender=Vessel)


# Handle Slug of Terminal

def create_terminal_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	# if new_slug is not None:
	# 	slug = new_slug
	# qs = Terminal.objects.filter(slug=slug).order_by("-id")
	# exists = qs.exists()
	# if exists:
	# 	new_slug = "%s-%s" %(slug, qs.first().id)
	# 	return create_terminal_slug(instance, new_slug=new_slug)
	return slug


def pre_save_terminal_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_terminal_slug(instance)

pre_save.connect(pre_save_terminal_receiver, sender=Terminal)


# Handle Slug of Service

def create_service_slug(instance, new_slug=None):
	slug = slugify(instance.name)
	# if new_slug is not None:
	# 	slug = new_slug
	# qs = Service.objects.filter(slug=slug).order_by("-id")
	# exists = qs.exists()
	# if exists:
	# 	new_slug = "%s-%s" %(slug, qs.first().id)
	# 	return create_service_slug(instance, new_slug=new_slug)
	return slug


def pre_save_service_receiver(sender, instance, *args, **kwargs):
	if not instance.slug:
		instance.slug = create_service_slug(instance)

pre_save.connect(pre_save_service_receiver, sender=Service)



# Handle Slug of Voy
# Original function , comment on June 18,2021
# def create_voy_slug(instance, new_slug=None):
#     slug = slugify(instance.voy + '-' + instance.code)
#     print ('New slug %s' % slug)
#     if new_slug is not None:
#         slug = new_slug
#     qs = Voy.objects.filter(slug=slug).order_by("-id")
#     # qs = Voy.objects.filter(voy=instance.voy).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         # new_slug = "%s-%s" %(slug, qs.first().performa_in.strftime("%Y-%m-%d"))
#         new_slug = "%s-%s" %(slug, qs.count()+1)
#         print ('New slug %s' % new_slug)
#         return create_voy_slug(instance, new_slug=new_slug)
#     return slug

def create_voy_slug(instance, new_slug=None):
	slug = slugify(instance.voy + '-' + instance.code)
	print (f'New voy {instance} ,slug is {slug}')
	if new_slug is not None:
	    slug = new_slug
	qs = Voy.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()
	if exists:
	    new_slug =slugify( "%s-%s-%s" %(instance.voy,instance.code,instance.id))
	    print ('New slug %s' % new_slug)
	    return create_voy_slug(instance, new_slug=new_slug)
	return slug


def pre_save_voy_receiver(sender, instance, *args, **kwargs):
	# print ('Presave Trigger')
	#To support Save as Draft 
	if not instance.slug:
		instance.slug = create_voy_slug(instance)
	# if not instance.slug:
	# 	instance.slug = create_voy_slug(instance)

pre_save.connect(pre_save_voy_receiver, sender=Voy)



# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     # uploads/%Y/%m/%d/
#     return '%s/%s'.format(%Y,%m,%d)

class ReportFile(models.Model):
	week_name = models.CharField(max_length=100)
	current_week = models.FileField(upload_to='uploads/%Y/%m/%d/')
	next_week = models.FileField(upload_to='uploads/%Y/%m/%d/')
	remark = models.TextField(blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	# user = models.ForeignKey('auth.User',blank=True,null=True)
	user = models.ForeignKey('auth.User',blank=True,null=True,on_delete=models.SET_NULL)

	def __str__(self):
		return ('%s' % (self.week_name))

	# def get_current_absolute_url(self):
	#     from django.urls import reverse
	#     return reverse('people.views.details', args=[str(self.id)])

# Add new for cutoff setting
class cutoff(models.Model):
	# voy = models.ForeignKey(Voy)
	voy = models.ForeignKey(Voy,on_delete=models.CASCADE)
	dry_date = models.DateTimeField(verbose_name ='Dry CutOff',blank=True, null=True)
	reef_date = models.DateTimeField(verbose_name ='Reef CutOff',blank=True, null=True)
	chilled_date = models.DateTimeField(verbose_name ='Chilled CutOff',blank=True, null=True)
	durian_date = models.DateTimeField(verbose_name ='Durian/Longan CutOff',blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	# user = models.ForeignKey('auth.User',blank=True,null=True)
	user = models.ForeignKey('auth.User',blank=True,null=True,on_delete=models.SET_NULL)
	remark = models.TextField(max_length=255,blank=True, null=True)

	def __str__(self):
		return ('%s' % (self.voy))

	def get_absolute_url(self):
		return reverse('berth:cutoff-detail', kwargs={'pk': self.pk})


