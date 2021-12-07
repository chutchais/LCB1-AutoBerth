from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)

from berth.models import Voy
from berth.models import Vessel

# Added by CHutchai on March 26,2019
# To support new company , that provide Berth schedule
class BerthSerializer(ModelSerializer):
	class Meta:
		model = Voy
		# fields ='__all__'
		fields =['service','vessel','code','voy',
				'performa_in','performa_out','eta','etb','etd',
				'terminal','vsl_oper','imp_release_date']


class VoySerializer(ModelSerializer):
	lov = SerializerMethodField()
	vessel_type  = SerializerMethodField()
	color = SerializerMethodField()
	slug = SerializerMethodField()
	startCol = SerializerMethodField()
	stopCol = SerializerMethodField()
	move_performa = SerializerMethodField()
	callsign = SerializerMethodField()
	imo = SerializerMethodField()
	class Meta:
		model = Voy
		# fields ='__all__'
		fields =['service','vessel','code','voy',
				'performa_in','performa_out','eta','etb','etd',
				'lov','dis_no','load_no','est_teu',
				'terminal','start_pos','vessel_type','color','remark',
				'vsl_oper','arrival_draft','departure_draft','slug','draft',
				'startCol','stopCol','move_performa','move_confirm','text_pos','qc','inverse',
				'dis_fross_weight','load_gross_weight','callsign','imo']

	def get_lov(self,obj):
		# content_type = obj.get_content_type
		# object_id=obj.id
		# c_qs = Comment.objects.filter_by_instance(obj)
		# comments = CommentSerializer(c_qs,many=True).data
		return obj.vessel.lov

	def get_vessel_type(self,obj):
		return obj.vessel.v_type

	def get_color(self,obj):
		return obj.service.color

	def get_slug(self,obj):
		return obj.slug

	def get_startCol(self,obj):
		return obj.terminal.start_range

	def get_stopCol(self,obj):
		return obj.terminal.stop_range

	def get_move_performa(self,obj):
		return obj.service.move_performa
	
	def get_callsign(self,obj):
		return obj.vessel.callsign

	def get_imo(self,obj):
		return obj.vessel.imo


class VoyDetailSerializer(ModelSerializer):
	lov = SerializerMethodField()
	vessel_type  = SerializerMethodField()
	color = SerializerMethodField()
	slug = SerializerMethodField()
	startCol = SerializerMethodField()
	stopCol = SerializerMethodField()
	callsign = SerializerMethodField()
	imo = SerializerMethodField()

	class Meta:
		model = Voy
		# fields ='__all__'
		fields =['service','vessel','code','voy',
				'performa_in','performa_out','eta','etb','etd',
				'lov','dis_no','load_no','est_teu',
				'terminal','start_pos','vessel_type','color','remark',
				'vsl_oper','arrival_draft','departure_draft','slug','draft',
				'startCol','stopCol',
				'dis_fross_weight','load_gross_weight','callsign','imo']

	def get_lov(self,obj):
		return obj.vessel.lov

	def get_vessel_type(self,obj):
		return obj.vessel.v_type

	def get_color(self,obj):
		return obj.service.color

	def get_slug(self,obj):
		return obj.slug

	def get_startCol(self,obj):
		return obj.terminal.start_range

	def get_stopCol(self,obj):
		return obj.terminal.stop_range

	def get_callsign(self,obj):
		return obj.vessel.callsign

	def get_imo(self,obj):
		return obj.vessel.imo

# Added on Oct 19,2021
class TruckWindowSerializer(ModelSerializer):
	class Meta:
		model = Voy
		fields =['service','vessel','code','voy',
				'performa_in','performa_out','eta','etb','etd',
				'terminal','vsl_oper','imp_release_date','imp_release_date',
				'export_cutoff_date']
