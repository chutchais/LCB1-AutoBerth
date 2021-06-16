from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)

from rest_framework import serializers

from bayplan.models import BayPlanFile
from container.models import Container
from container.api.serialize import ContainerListSerializer

class BayPlanSerializer(ModelSerializer):
	url = serializers.CharField(source='get_absolute_url', read_only=True)
	class Meta:
		model = BayPlanFile
		# fields ='__all__'
		exclude = ('voy','created_date','modified_date','user',)
		# fields =['voy','filename','slug','uploaded','upload_date','upload_date']

class BayPlanDetailSerializer(ModelSerializer):
	voy  = SerializerMethodField()
	vessel_code  = SerializerMethodField()
	container_set = ContainerListSerializer(many=True, read_only=True)
	class Meta:
		model = BayPlanFile
		# fields ='__all__'
		fields =['voy','vessel_code','slug','container_set']
	
	def get_vessel_code(self,obj):
		return obj.voy.code

	def get_voy(self,obj):
		return obj.voy.voy

class BayPlanUpdateSerializer(ModelSerializer):
	class Meta:
		model = BayPlanFile
		fields =[
			'uploaded',
			'upload_date'
		]

# class VoySerializer(ModelSerializer):
# 	lov = SerializerMethodField()
# 	vessel_type  = SerializerMethodField()
# 	color = SerializerMethodField()
# 	slug = SerializerMethodField()
# 	startCol = SerializerMethodField()
# 	stopCol = SerializerMethodField()
# 	move_performa = SerializerMethodField()
# 	class Meta:
# 		model = Voy
# 		# fields ='__all__'
# 		fields =['service','vessel','code','voy',
# 				'performa_in','performa_out','eta','etb','etd',
# 				'lov','dis_no','load_no','est_teu',
# 				'terminal','start_pos','vessel_type','color','remark',
# 				'vsl_oper','arrival_draft','departure_draft','slug','draft',
# 				'startCol','stopCol','move_performa','move_confirm','text_pos','qc','inverse']

# 	def get_lov(self,obj):
# 		# content_type = obj.get_content_type
# 		# object_id=obj.id
# 		# c_qs = Comment.objects.filter_by_instance(obj)
# 		# comments = CommentSerializer(c_qs,many=True).data
# 		return obj.vessel.lov

# 	def get_vessel_type(self,obj):
# 		return obj.vessel.v_type

# 	def get_color(self,obj):
# 		return obj.service.color

# 	def get_slug(self,obj):
# 		return obj.slug

# 	def get_startCol(self,obj):
# 		return obj.terminal.start_range

# 	def get_stopCol(self,obj):
# 		return obj.terminal.stop_range

# 	def get_move_performa(self,obj):
# 		return obj.service.move_performa


# class VoyDetailSerializer(ModelSerializer):
# 	lov = SerializerMethodField()
# 	vessel_type  = SerializerMethodField()
# 	color = SerializerMethodField()
# 	slug = SerializerMethodField()
# 	startCol = SerializerMethodField()
# 	stopCol = SerializerMethodField()
# 	class Meta:
# 		model = Voy
# 		# fields ='__all__'
# 		fields =['service','vessel','code','voy',
# 				'performa_in','performa_out','eta','etb','etd',
# 				'lov','dis_no','load_no','est_teu',
# 				'terminal','start_pos','vessel_type','color','remark',
# 				'vsl_oper','arrival_draft','departure_draft','slug','draft',
# 				'startCol','stopCol']

# 	def get_lov(self,obj):
# 		# content_type = obj.get_content_type
# 		# object_id=obj.id
# 		# c_qs = Comment.objects.filter_by_instance(obj)
# 		# comments = CommentSerializer(c_qs,many=True).data
# 		return obj.vessel.lov

# 	def get_vessel_type(self,obj):
# 		return obj.vessel.v_type

# 	def get_color(self,obj):
# 		return obj.service.color

# 	def get_slug(self,obj):
# 		return obj.slug

# 	def get_startCol(self,obj):
# 		return obj.terminal.start_range

# 	def get_stopCol(self,obj):
# 		return obj.terminal.stop_range
