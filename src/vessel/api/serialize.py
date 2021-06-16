from rest_framework.serializers import (
	ModelSerializer,
	HyperlinkedIdentityField,
	SerializerMethodField
	)

# from berth.models import Voy
from berth.models import Vessel



class VesselSerializer(ModelSerializer):
	# lov = SerializerMethodField()
	# vessel_type  = SerializerMethodField()
	# color = SerializerMethodField()
	class Meta:
		model = Vessel
		fields ='__all__'
		# fields =['service','vessel','code','voy',
		# 		'performa_in','performa_out','eta','etb','etd',
		# 		'lov','dis_no','load_no','est_teu',
		# 		'terminal','start_pos','vessel_type','color','remark',
		# 		'vsl_oper','arrival_draft','departure_draft']

	# def get_lov(self,obj):
	# 	# content_type = obj.get_content_type
	# 	# object_id=obj.id
	# 	# c_qs = Comment.objects.filter_by_instance(obj)
	# 	# comments = CommentSerializer(c_qs,many=True).data
	# 	return obj.vessel.lov

	# def get_vessel_type(self,obj):
	# 	return obj.vessel.v_type

	# def get_color(self,obj):
	# 	return obj.vessel.color


class VesselDetailSerializer(ModelSerializer):
	# color = SerializerMethodField()
	class Meta:
		model = Vessel
		# fields ='__all__'
		fields =['name','slug','description','lov','imo','v_type','status']

	# def get_color(self,obj):
	# 	return obj.colo
# class VesselDetailSerializer(ModelSerializer):
# 	color = SerializerMethodField()
# 	class Meta:
# 		model = Vessel
# 		# fields ='__all__'
# 		fields =['name','slug','description','lov','imo','color','v_type','status']

# 	def get_color(self,obj):
# 		return obj.color

