from django import template
register = template.Library()

from datetime import datetime, date
from dateutil.relativedelta import relativedelta

@register.filter
def init_incident_date_querystring(no_prev_month):
    current_date = date.today()
    prev1M_from_current_date = current_date + relativedelta(months=-int(no_prev_month))

    str_current_date = current_date.strftime("%Y-%m-%d")
    str_prev1M_from_current_date = prev1M_from_current_date.strftime("%Y-%m-%d")
    myfilter_date = {'incident_datetime__gt': str_current_date, 'incident_datetime__lt': str_prev1M_from_current_date}

    return f"incident_datetime__lt={str_current_date}&incident_datetime__gt={str_prev1M_from_current_date}"