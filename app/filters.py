import django_filters

from django.utils.translation import gettext as _
from django_filters import *

from app.models import *
from app.forms  import  MyDateInput,MyDateTimeInput,MyTimeInput
from datetime import timedelta

from django.db.models import Q

import datetime as datetime
import datetime as date

class MyEndDateFilter(django_filters.DateFilter):

    def filter(self, qs, value):
        if value:
            value = value + timedelta(1)
        return super(MyEndDateFilter, self).filter(qs, value)


def active_engineer_incident_owner(request):
    return Employee.objects.filter(is_inactive=False)

def company_for_project_by_role(request):
    if request is None:
        return Company.objects.all()
    elif request.user.is_superuser:
    # elif request.user.is_staff or  request.user.is_superuser:
        return Company.objects.filter(is_customer=True)
    else:
        # next version
        # is_in_manager_group = Manager.objects.filter(user_id__exact=request.user.id,is_site_manager__exact=True).exists()
        # is_in_office_admin_group = OfficeAdmin.objects.filter(user_id__exact=request.user.id).exists()
        # return Company.objects.filter(manager__user=request.user, is_customer=is_in_manager_group,is_for_office_admin=is_in_office_admin_group)

        manager_comp= Company.objects.filter(manager__user=request.user,is_customer=True)
        engineer_comp=Company.objects.filter(engineer__user=request.user,is_customer=True)
        if manager_comp.count() > 0:
            return manager_comp
        elif engineer_comp.count() > 0:
            return engineer_comp
        else:
            return None
        #return Company.objects.filter( ( Q(manager__user=request.user) | Q(engineer__user=request.user)), is_customer=True)

class ProjectFilter(django_filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset = company_for_project_by_role, field_name='company',
                                        label='Company')
    # company = filters.ModelChoiceFilter(queryset=Company.objects.filter(is_customer=True),field_name='company',label='Company',required=True)

    #is_dummy = django_filters.BooleanFilter(field_name='is_dummy', label="Project-Dummy", required=True)

    enq_id = django_filters.CharFilter(lookup_expr='icontains', field_name='enq_id', label='ENQ')
    project= django_filters.CharFilter(lookup_expr='icontains', field_name='project_name',label='Project')

    class Meta:
        model = Project
        fields = ['is_dummy']
    def __init__(self, *args, author=None, **kwargs):
      super().__init__(*args, **kwargs)
      self.form.initial['is_dummy'] = 'No'


class  InventoryFilter(django_filters.FilterSet):

   company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='project__company', label='Company')
   # project_title= django_filters.CharFilter(lookup_expr='icontains',field_name='project__project_name',label='Project')
   is_dummy = django_filters.BooleanFilter(field_name='is_dummy', label="Inventory-Dummy", required=True,)
   enq_id = django_filters.CharFilter(lookup_expr='icontains',  field_name='project__enq_id', label='ENQ')
   devicename_hostname = django_filters.CharFilter(lookup_expr='icontains', field_name='devicename_hostname', label='Device/Host Name')

   product_type= django_filters.ModelChoiceFilter(queryset=Product_Type.objects.all(), field_name='product_type', label='Product-Type')
   brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all(), field_name='brand', label='Brand')

   is_managed_by_admin=django_filters.BooleanFilter(field_name='project__company__is_managed_by_admin', label="Yes=For Admin , No=For SM", required=True)

   # customer_warranty_end__gte = django_filters.DateFilter(field_name='customer_warranty_end', lookup_expr='gte'
   #                                                   ,
   #                                                   widget=MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
   #                                                   label="In-CustWarranty")

   class Meta:
     model=Inventory
     fields=['serial_number']


class  InventoryToChangeInIncidentFilter(django_filters.FilterSet):

   enq_id = django_filters.CharFilter(lookup_expr='icontains',field_name='project__enq_id', label='ENQ',required=True)
   product_type = django_filters.ModelChoiceFilter(queryset=Product_Type.objects.all(), field_name='product_type',
                                                   label='Product-Type')
   brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all(), field_name='brand', label='Brand')

   class Meta:
     model=Inventory
     fields=['serial_number']


class IncidentFilter(django_filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='inventory__project__company', label='Company')
    # project = django_filters.CharFilter(lookup_expr='icontains',field_name= 'inventory__project__project_name',label='Project-Title' )

    incident_datetime__gt = django_filters.DateFilter(field_name='incident_datetime', lookup_expr='gt'
                                                      ,widget= MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),label="Incident Date From" ,required=True)
    incident_datetime__lt = MyEndDateFilter(field_name='incident_datetime', lookup_expr='lt'
                                                      ,widget= MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),label="Incident Date To",required=True)

    enq_id = django_filters.CharFilter(lookup_expr='icontains',field_name='inventory__project__enq_id', label='ENQ')
    incident_no=django_filters.CharFilter(lookup_expr='icontains', field_name='incident_no',label='Incident-No')
    incident_subject = django_filters.CharFilter(lookup_expr='icontains', field_name='incident_subject', label='Subject',)


    serial_number = django_filters.CharFilter(field_name='inventory__serial_number', label='Serial')

    brand = django_filters.ModelChoiceFilter(queryset=Brand.objects.all(), field_name='inventory__brand', label='Brand')

    incident_owner = filters.ModelChoiceFilter(queryset = active_engineer_incident_owner, field_name='incident_owner',
                                        label='Engineer Owner')

    class Meta:
        model = Incident

        fields = ['incident_status','incident_severity']







class DetailFilter(django_filters.FilterSet):
    task_start__gt = django_filters.DateFilter(field_name='task_start', lookup_expr='gt',
                                                      widget=MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
                                                      label="Task Start From")
    task_end__lt = MyEndDateFilter(field_name='task_start', lookup_expr='lt',
                                                      widget=MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
                                                      label="To")
    class Meta:
        model= Incident_Detail
        #fields=['service_team','employee']
        fields = ['service_team']



class CustomerSupportFilter(django_filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='company',
                                        label='Customer-Company', required=True)
    customer_name = django_filters.CharFilter(lookup_expr='icontains', field_name='customer_name', label='Customer Name')
    class Meta:
        model=Customer
        fields=['is_active']

class ProductSupportFilter(django_filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='customer_company',
                                        label='Customer-Company', required=True)
    company_product = filters.ModelChoiceFilter(queryset=Company.objects.filter(is_subcontractor=True), field_name='partner_company',
                                        label='Partner-Company')
    product_name = django_filters.CharFilter(lookup_expr='icontains', field_name='product_name', label='Product Partner Name')
    class Meta:
        model=Product
        fields=['is_active']


class BranchFilter(django_filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='company',
                                        label='Company', required=True)
    branch_name = django_filters.CharFilter(lookup_expr='icontains', field_name='branch_name', label='Branch Name')
    class Meta:
        model=Branch
        exclude = ['address','customer']
class DataCenterFilter(django_filters.FilterSet):
    company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='company',
                                        label='Company', required=True)
    datacenter_name = django_filters.CharFilter(lookup_expr='icontains', field_name='datacenter_name', label='DataCenter Name')
    class Meta:
        model=DataCenter
        exclude = ['address']


class  PMFilter(django_filters.FilterSet):

   company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='project__company', label='Company')
   enq_id = django_filters.CharFilter(lookup_expr='icontains',  field_name='project__enq_id', label='ENQ')
   planned_date__gt = django_filters.DateFilter(field_name='planned_date', lookup_expr='gte',
                                                     widget=MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
                                                     label="PMPlan From", required=True , help_text="The first day of the month")
   planned_date__lt = django_filters.DateFilter(field_name='planned_date', lookup_expr='lte',
                                                     widget=MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
                                                     label="To", required=True , help_text="The last day of the month")
   # planned_date__lt = MyEndDateFilter(field_name='planned_date', lookup_expr='lte', widget=MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
   #                                         label="To", required=True,help_text="The last day of the month")
   class Meta:
     model=PreventiveMaintenance
     exclude = ['remark']

class  PMSummaryFilter(django_filters.FilterSet):

   company = filters.ModelChoiceFilter(queryset=company_for_project_by_role, field_name='project__company', label='Company', required=True)
   enq_id = django_filters.CharFilter(lookup_expr='icontains',  field_name='project__enq_id', label='ENQ')
   class Meta:
     model=PreventiveMaintenance
     exclude = ['remark','planned_date']

def brand_for_pm(request):
    listIDs = request.session.get("listBrandIDByPMItems", None)
    if listIDs is None:
        return Brand.objects.all()
    else:
        return Brand.objects.filter(id__in=listIDs)

class  PMInventoryItemFilter(django_filters.FilterSet):
    # product_type = django_filters.ModelChoiceFilter(queryset=Product_Type.objects.all(), field_name='product_type',
    #                                                 label='Product-Type',required=True)
    is_pm = django_filters.BooleanFilter(field_name='is_pm', label="Is PM", required=True)
    brand = django_filters.ModelChoiceFilter(queryset=brand_for_pm, field_name='inventory__brand', label='Brand',required=True)
    model=PM_Inventory
    exclude = ['remark']




