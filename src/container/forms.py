from django.forms import ModelForm
from .models import Container
from django import forms
import re
# from .views import under_deck,over_deck,tier1

class ContainerForm(ModelForm):
	# bay = forms.CharField(required=False)
	# tier = forms.CharField(required=False)
	# row = forms.CharField(required=False)


	class Meta:
		model = Container
		fields = ['stowage']

	def clean_stowage(self):
		under_deck = ['18','16','14','12','10','08','06','04','02']
		# over_deck =['94','92','90','88','86','84','82','80']
		over_deck =['94','92','90','88','86','84','82','80','78','76','74','72']
		tier1 =['18','16','14','12','10','08','06','04','02','00','01','03','05','07','09','11','13','15','17']
		# tier2 =['16','14','12','10','08','06','04','02','00','01','03','05','07','09','11','13','15']
		import re
		# rex = re.compile("^[0-9]{5,6}$")
		rex = re.compile("^[0-9]{6}$") # 6 digits of stowage
		stowage = self.cleaned_data.get("stowage")
		# if  len(stowage) < 5 or len(stowage) > 6:
		# 	raise forms.ValidationError('Not a valid Slot , it should be 5 or 6 digit')
		# if  not rex.match(stowage):
		# 	raise forms.ValidationError('Not a valid Slot , only accept numeric')
		# return stowage
		if  len(stowage)!= 6:
			raise forms.ValidationError('Invalid Slot , it must be 6 digit')
		if  not rex.match(stowage):
			raise forms.ValidationError('Invalid Slot , accept only numeric')
		if stowage[:2]=='00':
			raise forms.ValidationError('Bay 00 dost not exist..')
		if not stowage[2:4] in tier1 :
			raise forms.ValidationError('Invalid slot, %s dost not exist tier list' % stowage[2:4])
		if not (stowage[-2:] in under_deck or stowage[-2:] in over_deck) :
			raise forms.ValidationError('Invalid slot, %s dost not exist row list' % stowage[-2:])
		return stowage

	def __init__(self,stowage=None,*args,**kwargs):
		# voy = kwargs.pop('voy')
		# print(voy_slug)
		# print (voy)
		# print (kwargs)
		# voy = kwargs.pop('voy')
		super(ContainerForm,self).__init__(*args,**kwargs)
		# self.fields['voy'].queryset = Voy.objects.all()

	def save(self, commit=True):
		container = super(ContainerForm, self).save(commit=False)
		# print ('Current stowage %s' % container.stowage)
		container.new_stowage = container.stowage
		container.bay=container.stowage[:1] if len(container.stowage)==5 else container.stowage[:2]
		container.ready_to_load = True
		container.uploaded = False
		if commit:
			container.save()
		return container