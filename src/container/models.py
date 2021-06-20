from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.urls import reverse
from colorfield.fields import ColorField

from bayplan.models import BayPlanFile

# Create your models here.
ACTIVE='A'
DEACTIVE='D'
STATUS_CHOICES = (
        (ACTIVE, 'Active'),
        (DEACTIVE, 'Deactive'),
    )

class DischargePort(models.Model):
	name = models.CharField(max_length=5,primary_key=True)
	slug = models.SlugField(unique=True,blank=True, null=True)
	description = models.CharField(max_length=255,blank=True, null=True)
	color = ColorField(default='#CCFFFF')
	status = models.CharField(max_length=1,choices=STATUS_CHOICES,default=ACTIVE)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	# user = models.ForeignKey('auth.User',blank=True,null=True)
	user = models.ForeignKey('auth.User',blank=True,null=True,on_delete=models.SET_NULL)
	
	def __str__(self):
		return self.name

class Container(models.Model):
	bayplanfile = models.ForeignKey(BayPlanFile,on_delete=models.CASCADE)
	slug = models.SlugField(unique=True,blank=True, null=True)
	item_no = models.IntegerField()
	container = models.CharField(max_length=11)
	iso_code  = models.CharField(max_length=10,blank=True, null=True)
	full	  = models.BooleanField(default=False)
	partner	  = models.CharField(max_length=10,blank=True, null=True)
	weight	  = models.IntegerField()
	load_port = models.CharField(max_length=10,blank=True, null=True)
	dis_port  = models.ForeignKey(DischargePort,blank=True, null=True,on_delete=models.SET_NULL)
	# dis_port  = models.CharField(max_length=10,blank=True, null=True)
	deliverly_port = models.CharField(max_length=10,blank=True, null=True)
	good_desc = models.CharField(max_length=100,blank=True, null=True)
	stowage =	models.CharField(max_length=10)
	original_stowage = models.CharField(max_length=10,blank=True, null=True)
	bay       =	models.CharField(max_length=10,blank=True, null=True)
	original_bay       =	models.CharField(max_length=10,blank=True, null=True)
	ready_to_load		= models.BooleanField(default=False)# Ready to UpLoad
	imdg = models.CharField(max_length=10,blank=True, null=True)
	un_no = models.CharField(max_length=10,blank=True, null=True)
	on_deck = models.BooleanField(default=False)
	uploaded = models.BooleanField(default=False)
	upload_date = models.DateTimeField(blank=True, null=True)
	created_date = models.DateTimeField(auto_now_add=True)
	modified_date = models.DateTimeField(blank=True, null=True,auto_now=True)
	# user = models.ForeignKey('auth.User',blank=True,null=True)
	user = models.ForeignKey('auth.User',blank=True,null=True,on_delete=models.SET_NULL)

	def __str__(self):
		return ('%s' % (self.container))

	def get_absolute_url(self):
		return reverse('container:stowage', kwargs={'slug': self.slug})

	def get_dischart_style(self):
		if self.dis_port.color:
			return ('style="background-color:%s" class="text-center"' % self.dis_port.color)

	def get_tooltip(self):
		# return ('No :%s    \
		# 	Disch Port : %s \
		# 	Weight : %s Kgs    \
		# 	ISO: %s ,F/E : %s' % (self.container,self.dis_port,self.weight,self.iso_code,'FULL' if self.full else 'MTY'))
		if self.imdg :
			# return ('IMDG: %s ' % (self.imdg))
			return ('%s' % (self.container))#for mobie
		else:
			return ('%s' % (self.container))#for mobie
			# return ('ISO: %s ,F/E : %s' % (self.iso_code,'FULL' if self.full else 'MTY'))


# def create_container_slug(instance, new_slug=None):
#     slug = slugify("%s-%s" %(instance.container, instance.item_no))
#     if new_slug is not None:
#         slug = new_slug
#     qs = Container.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" %(slug, qs.count())
#         return create_container_slug(instance, new_slug=new_slug)
#     return slug

def create_container_slug(instance, new_slug=None):
	from datetime import datetime
	slug = slugify(f'{instance.container}{instance.item_no} + "-" + {datetime.now().strftime("%dT%H:%M:%S")}')
	print (f'New Container {instance} ,slug is {slug}')
	return slug


def pre_save_container_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_container_slug(instance)

pre_save.connect(pre_save_container_receiver, sender=Container)


# def create_disport_slug(instance, new_slug=None):
#     slug = slugify("%s" %(instance.name))
#     if new_slug is not None:
#         slug = new_slug
#     qs = DischargePort.objects.filter(slug=slug).order_by("-id")
#     exists = qs.exists()
#     if exists:
#         new_slug = "%s-%s" %(slug, qs.count())
#         return create_disport_slug(instance, new_slug=new_slug)
#     return slug

def create_disport_slug(instance, new_slug=None):
	from datetime import datetime
	slug = slugify(f'{instance.name}')
	print (f'New DischargePort {instance} ,slug is {slug}')
	return slug


def pre_save_disport_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_disport_slug(instance)

pre_save.connect(pre_save_disport_receiver, sender=DischargePort)