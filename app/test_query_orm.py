from .models import *
from django.db.models import Q
def orm_query1(request):

 managers=list(Manager.objects.values())
 list_manger_user_id=[ x['user_id'] for x in managers ]
 list_manger_user_id.append(1)# admin
 user_list=User.objects.filter(~Q(id__in=list_manger_user_id))

 return user_list
