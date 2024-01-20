from django import template
from django.contrib.auth.models import Group

from app.models import *

from django.http import HttpResponse,HttpResponseRedirect

register = template.Library()
# site manger who can manipulate data
@register.filter(name='has_group')
def has_group(user, group_name):

    is_existing=  Manager.objects.filter(user_id__exact=user.id,is_site_manager__exact=True).exists()
    return is_existing
# site manger and engineer

# they are in manager grop but just vew data (is_manager=False)
@register.filter(name='has_group_viewer')
def has_group_viewer(user, group_name):

    is_existing=  Manager.objects.filter(user_id__exact=user.id).exists()
    return is_existing


# site manger and engineer
@register.filter(name='has_group_update_pm_item')
def has_group_update_pm_item(user, group_name):
        is_existing = Manager.objects.filter(user_id__exact=user.id, is_site_manager__exact=True).exists()
        if is_existing==False:
            is_existing = Engineer.objects.filter(user_id__exact=user.id).exists()
        return is_existing

    # group = Group.objects.get(name=group_name)
    # return True if group in user.groups.all() else False

# {% if request.user|has_group:"site-manager" %}
#   <div class='row text-center'>
#                     <div class="col-md-12 center-block">
#                         <input type="submit" value="Save Incident" class="btn btn-success"
#                                onclick="return confirm('Do you want to save?')">
#                     </div>
#                 </div>
#
# {% endif %}

