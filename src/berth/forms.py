from django.forms import ModelForm
from .models import cutoff,Voy

class CutoffForm(ModelForm):
	class Meta:
		model = cutoff
		fields = ['return_date','dry_date','reef_date','chilled_date','durian_date','remark']

	def __init__(self,voy=None,*args,**kwargs):
		# voy = kwargs.pop('voy')
		# print(voy_slug)
		# print (voy)
		print (kwargs)
		# voy = kwargs.pop('voy')
		super(CutoffForm,self).__init__(*args,**kwargs)
		# self.fields['voy'].queryset = Voy.objects.all()

	# def __init__(self, *args, **kwargs):
	# 	user = kwargs.pop('user')
	# 	super(FolderForm, self).__init__(*args, **kwargs)
	# 	self.fields['parent'].queryset = Folder.objects.filter(user=user)