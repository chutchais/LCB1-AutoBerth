from django import template
from datetime import timedelta
from django.db.models import Avg,Sum
import datetime

register = template.Library()

import os


# @register.assignment_tag
@register.simple_tag
def is_readytoload(load_number):
	if load_number > 0:
		vType='ok'
		vColor='success'
		return 'class=\"glyphicon glyphicon-%s text-%s\"' % (vType,vColor)
	else:
		vType='remove'
		vColor='danger'
		return ''


# @register.assignment_tag
@register.simple_tag
def get_weight(obj_list,stowage):
	# print(obj_list)
	# print(stowage)
	try :
		x = next(y for y in obj_list if y[0]==stowage)
		return x[1]
	except:
		return 0


# @register.assignment_tag
@register.simple_tag
def percent(x,total):
	# print (obj.strip())
	if x:
		return (x/total)*100
	else:
		return 0
		
# @register.assignment_tag
@register.simple_tag
def sum(obj,field):
	# print (obj.strip())
	return obj.aggregate(Sum(field))

# @register.assignment_tag
@register.simple_tag
def weight(x):
	y=str(x)
	return ('%s.%s' % (y[:-3],y[2:3]))

# @register.assignment_tag
@register.simple_tag
def combine_stowage(bay,tier,row):
	return ('%s%s%s' % (bay,tier,row))

# @register.assignment_tag
@register.simple_tag
def first_container(obj,stowage):
	return obj.filter(stowage=stowage).first()

# @register.assignment_tag
@register.simple_tag
def original_container(obj,stowage):
	return obj.filter(original_stowage=stowage).first()

# @register.assignment_tag
@register.simple_tag
def get_container_by_original_stowage(obj_list,slot):
	for obj in obj_list:
		if obj.original_stowage == slot:
			return obj

# @register.assignment_tag
@register.simple_tag
def get_container_by_stowage(obj_list,slot):
	for obj in obj_list:
		if obj.stowage == slot:
			# print (obj.container,obj.get_dischart_style)
			return obj

# @register.assignment_tag
@register.simple_tag
def get_position_by_stowage(slot):
	row = slot[-2:]
	if int(row) > 70:
		return 'OD'
	if int(row) < 30:
		return 'UD'


@register.filter
def in_stowage(obj, stowage):
    return obj.filter(stowage = stowage)

@register.filter
def in_stowage_list(obj_list, slot):
	objQ=[]
	for obj in obj_list:
		if obj.stowage == slot:
			objQ.append(obj)
	# print (objQ)
	return objQ

@register.filter
def original_stowage(obj, stowage):
    return obj.filter(original_stowage = stowage)

@register.filter
def in_bay(obj, bay):
    return obj.filter(bay__startswith =bay)

@register.filter
def filename(value):
    return os.path.basename(value.file.name)


# @register.assignment_tag
@register.simple_tag
def cut(service):
	return service.__str__().split('-')[0]


# @register.assignment_tag
@register.simple_tag
def is_arrive(etb,etd):
	if etb < datetime.datetime.now():
		if etd < datetime.datetime.now():
			return 'Departed'
		return 'Arrived'
	else:
		return '...'


# @register.assignment_tag
@register.simple_tag
def is_fix_cutoff(service):
	strService = service.__str__().split('-')[0]
	service_lists = ['BOOM','HORN','SE1','ANX','TR1','TR2','NTX','PH4','IA2',
					'THAI2','THAI2A','THAI2B','009','TP11','SEA1','SEA2','PH5']#{'BOOM','HORN','SE1','ANX'.'TR1','NTX','PH4','IA2'}
	if strService in  service_lists :
		# print(service)
		return True

# @register.assignment_tag
@register.simple_tag
def is_overdue(perform_date):
	import datetime
	now = datetime.datetime.now()

	# print (perform_date)
	if perform_date == None:
		print ('perform_date is None')
		return ''

	if perform_date < now:
		# print((now-perform_date).total_seconds()/60)
		return 'class= danger'
	# else:
	# 	minutediff = (perform_date-now).total_seconds()/60
	# 	return 'class=alert-warning' if minutediff <60 else ''

# @register.assignment_tag
@register.simple_tag
def is_overhour(etb_date,perform_date):
	if etb_date > perform_date:
		minutediff = (etb_date-perform_date).total_seconds()/60
	else:
		minutediff = (perform_date-etb_date).total_seconds()/60

	return 'class=alert-warning' if minutediff > (24*60) else ''


# @register.assignment_tag
@register.simple_tag
def set_to_Saturday(service,perform_date):
	strService = service.__str__()
	firstday = perform_date -  timedelta(days=perform_date.weekday())
	Saturday = firstday + datetime.timedelta( (5-firstday.weekday()) % 7 )
	if 'BOOM' in strService :
		return Saturday.replace(hour=5, minute=00)

	if 'HORN' in strService :
		return Saturday.replace(hour=12, minute=00)
	
	if '009' in strService :
		return Saturday.replace(hour=12, minute=00)
	
	if 'TP11' in strService :
		return Saturday.replace(hour=12, minute=00)


# @register.assignment_tag
@register.simple_tag
def decrease_hour(date_in,hour):
	return date_in - timedelta(hours=hour)


# @register.assignment_tag
@register.simple_tag
def increase_hour(date_in,hour):
	return date_in + timedelta(hours=hour)

# @register.assignment_tag
@register.simple_tag
def is_Boom_or_Horn(service):
	strService = service.__str__()
	# print (strService)
	return True if strService in ['BOOM','HORN','009'] else False

# @register.assignment_tag
@register.simple_tag
# ['BOOM','HORN','SE1','ANX'.'TR1','NTX','PH4','IA2']
def get_fix_cutoff(service,perform_date):
	strService = service.__str__()
	firstday = perform_date -  timedelta(days=perform_date.weekday())
	Monday = firstday + datetime.timedelta( (0-firstday.weekday()) % 7 )
	Tueday = firstday + datetime.timedelta( (1-firstday.weekday()) % 7 )
	Wednesday = firstday + datetime.timedelta( (2-firstday.weekday()) % 7 )
	Thursday = firstday + datetime.timedelta( (3-firstday.weekday()) % 7 )
	Friday = firstday + datetime.timedelta( (4-firstday.weekday()) % 7 )
	Saturday = firstday + datetime.timedelta( (5-firstday.weekday()) % 7 )
	Sunday = firstday + datetime.timedelta(days=6) #datetime.timedelta( (6-firstday.weekday()) % 7 )
	# print ('Get Fix %s' % strService)
	if 'BOOM' in strService :
		# return Saturday.replace(hour=5, minute=00) #Change on March 20,2018
		return Friday.replace(hour=20, minute=00)

	if 'HORN' in strService :
		# return Saturday.replace(hour=12, minute=00) #Change on March 20,2018
		return Sunday.replace(hour=4, minute=00)
	
	if '009' in strService :
    		# return Saturday.replace(hour=12, minute=00) #Change on March 20,2018
		return Sunday.replace(hour=4, minute=00)
	
	if 'TP11' in strService :
    		# return Saturday.replace(hour=12, minute=00) #Change on March 20,2018
		return Sunday.replace(hour=4, minute=00)

	if 'SE1' in strService :
		# print (Thursday)
		return Thursday.replace(hour=6, minute=00)

# Remove on Dec 21,2018
	# if 'ANX' in strService :
	# 	return Tueday.replace(hour=23, minute=59)

	if 'TR1' in strService :
		return Thursday.replace(hour=11, minute=00)
		
	if 'TR2' in strService :
		return Thursday.replace(hour=11, minute=00)

	if 'NTX' in strService :
		return Friday.replace(hour=18, minute=00)

	if 'PH4' in strService :
		return Saturday.replace(hour=2, minute=00)

	if 'IA2' in strService :
		# print('IA2 %s' % firstday)
		return Sunday.replace(hour=14, minute=00)

	if 'THAI2' in strService :
		# print('THAI2 %s' % firstday)
		return perform_date - datetime.timedelta(hours=12)
	
	if 'THAI2A' in strService :
    		# print('THAI2 %s' % firstday)
		return perform_date - datetime.timedelta(hours=12)
	
	if 'THAI2B' in strService :
    		# print('THAI2 %s' % firstday)
		return perform_date - datetime.timedelta(hours=12)
# Add on Dec 21,2018 
	if 'ANX' in strService :
		# print('ANX %s' % perform_date)
		return perform_date - datetime.timedelta(hours=12)
	# Add on March 12,2019
	if 'SEA1' in strService :
		return perform_date - datetime.timedelta(hours=12)

	if 'SEA2' in strService :
		return perform_date - datetime.timedelta(hours=12)

# Add on June 17,2019 
	if 'PH5' in strService :
		return Saturday.replace(hour=2, minute=00)



# @register.assignment_tag
# def strip(obj):
# 	# print (obj.strip())
# 	return obj.strip()

# @register.assignment_tag
# def is_boi(obj,machine):
# 	# print (obj.strip())
# 	return True if obj.strip() in machine.values_list('machine_name',flat=True) else False


# @register.assignment_tag
# def combine_date(year,month,day):
# 	# print (obj.strip())
# 	return ('%s-%s-%s' % (year,month,day))

def add( value, arg ):
	'''
	Divides the value; argument is the divisor.
	Returns empty string on any error.
	'''
	try:
	    value = int( value )
	    arg = int( arg )
	    if arg: return value + arg
	except: pass
	return ''
