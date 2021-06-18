import redis
db = redis.StrictRedis('berth-redis', 6379,db=0, charset="utf-8", decode_responses=True) #Production


def save_voy_to_redis(voy_obj):
    print(f'Start to save changed voy {voy_obj} to Redis')
    # from django.core.serializers import serialize
    # from berth.models import Voy
    # voy = Voy.objects.get(slug=slug)
    key = voy_obj.slug
    payload = voy_obj.json
    # json.dumps(json_dict)
    db.set(key,payload)
    ttl = 60 #1 minutes
    ttl = 60 * 60 * 24 * 30 # 90 days
    db.expire(key, ttl) #expire 90 days
    # 
    # db.publish('QUEUE',payload)
    print(f'Save changed voy to Redis .....Successful')