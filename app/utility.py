from datetime import datetime
from app.models import Company

def message_inaccessible_tasks(request,operation):
    return f'<h2>{request.user} are not authorized to {operation} of this company.</h2><b>Contact administrator to add this user to the manager OR engineer table in company</b>'

def list_customer_company(current_user):

   #list_cust_company= Company.objects.filter( is_customer=True,id__in=[2,1]).values_list('id','company_name','company_full_name')# ais and yip
   list_cust_company = Company.objects.filter(manager__user= current_user, is_customer=True) .values_list('id','company_name','company_full_name')

   list_x=[ (comp[0],f"{comp[1]} - {comp[2]}")  for comp in list_cust_company ]
   list_x_selection=tuple( list_x)
   return  list_x_selection  # value as dic in array
from django.conf import settings

def list_year_selection():
    currnet_year=datetime.now().year
    start_year=currnet_year-5
    list_year_selection=[]
    for year in range(currnet_year,start_year,-1):
      tuples_year=(str(year),str(year) )
      list_year_selection.append(tuples_year)
    return     list_year_selection

def list_quarter_selection():
    return  (
        ('0','YEAR'),
        ('1', 'Q1'),
        ('2', 'Q2'),
        ('3', 'Q3'),
        ('4', 'Q4')
    )


def get_period_selection(selected_year, selected_period):
    if selected_period == 0:
        start_x = datetime(selected_year, 1, 1)
        end_x =   datetime(selected_year, 12, 31)
    elif selected_period == 1:
        start_x = datetime(selected_year, 1, 1)
        end_x = datetime(selected_year, 3, 31)
    elif selected_period == 2:
        start_x = datetime(selected_year, 4, 1)
        end_x = datetime(selected_year, 6, 30)
    elif selected_period == 3:
        start_x = datetime(selected_year, 7, 1)
        end_x = datetime(selected_year, 9, 30)
    else:
        start_x = datetime(selected_year, 10, 1)
        end_x = datetime(selected_year, 12, 31)

    start_str = start_x.strftime("%Y-%m-%d")
    end_str = end_x.strftime("%Y-%m-%d")

    return start_str, end_str

import os
import sys
def add_error_to_file(error_des):
    "put error to  log file if database error"
    f = open(settings.LOG_ERROR_FILE_PATH, 'a')
    error_str = f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")}|{repr(error_des)}\n'
    f.write(error_str)
    f.close()
    print(error_str)
    #raise Exception(error_str)