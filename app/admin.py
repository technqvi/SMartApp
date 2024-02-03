from django.contrib import admin
from .models import *
from django.contrib.admin import SimpleListFilter
from django.contrib.admin.models import LogEntry

from models_logging.admin import HistoryAdmin
from django.db.models import Q
#from app.views import manage_sm
from django.template.response import TemplateResponse
from django.urls import path
from django import forms
import os


class CompanyFilter(SimpleListFilter):
    title = "Company"
    parameter_name = 'company'

    def lookups(self, request, model_admin):
        companyList = set([c.company for c in model_admin.model.objects.select_related('company').all()])
        return [(c.id, c.company_name) for c in companyList]

    def queryset(self, request, queryset):
        if self.value():
            try:
                company_id = int(self.value())
            except (ValueError):
                return queryset.none()
            else:
                return queryset.filter(company__id=company_id)

class BrandFilter(SimpleListFilter):
    title = "Brand"
    parameter_name = 'brand'

    def lookups(self, request, model_admin):
        brandList = set([c.brand for c in model_admin.model.objects.select_related('brand').all()])
        return [(c.id, c.brand_name) for c in brandList]

    def queryset(self, request, queryset):
        if self.value():
            try:
                brand_id = int(self.value())
            except (ValueError):
                return queryset.none()
            else:
                return queryset.filter(brand__id=brand_id)

class ModelFilter(SimpleListFilter):
    title = "Model"
    parameter_name = 'model'
    def lookups(self, request, model_admin):
        modelList = set([c.model for c in model_admin.model.objects.select_related('model').all()])
        return [(c.id, c.model_name) for c in modelList]
    def queryset(self, request, queryset):
        if self.value():
            try:
                model_id = int(self.value())
            except (ValueError):
                return queryset.none()
            else:
                return queryset.filter(model__id=model_id)
class MyCompanyAdminForm(forms.ModelForm):
    class Meta:

        model = Company
        widgets = {
              'manager':forms.CheckboxSelectMultiple
            }
        fields = '__all__'

class MyEngineerAdminForm(forms.ModelForm):
    class Meta:

        model = Engineer
        widgets = {
              'company':forms.CheckboxSelectMultiple
            }
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super(MyEngineerAdminForm, self).__init__(*args, **kwargs)
        self.fields['company'].queryset =Company.objects.filter(is_customer=True)



@admin.register(Engineer)
class EngineerAdmin(admin.ModelAdmin):
    actions = None
    list_display =('engineer_nickname','user')
    search_fields = ['engineer_nickname','user__first_name','user__last_name']
    form = MyEngineerAdminForm
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user"   :
            engineers = list(Engineer.objects.values())
            list_engineer_user_id = [x['user_id'] for x in engineers]
            list_engineer_user_id.append(1)  # always being admin

            managers = list(Manager.objects.values())
            list_manger_user_id = [x['user_id'] for x in managers]


            kwargs["queryset"] =User.objects.filter(~Q( id__in=list_engineer_user_id),~Q(id__in=list_manger_user_id),is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["user"]
        else:
            return []




@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    actions = None
    list_display =('company_name','is_customer','is_subcontractor','is_managed_by_admin')
    search_fields = ['company_name']
    list_filter = ['company_name']
    form=MyCompanyAdminForm

    # def get_readonly_fields(self, request, obj=None):
    #     if obj:
    #         return ["company_name"]
    #     else:
    #         return []
    def site_managers(self,obj):
        return " , ".join([ m.get_full_name() for m in obj.manager.all()])
    

@admin.register(SubCompany)
class SubCompanyAdmin(admin.ModelAdmin):
    actions = None
    list_display =('sub_company_name','head_company')
    search_fields = ['sub_company_name']
    list_filter = ['sub_company_name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "head_company":
            kwargs["queryset"] =Company.objects.filter(is_customer=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    actions = None
    list_display =('manager_nickname','user','is_site_manager')
    search_fields = ['manager_nickname','user__first_name','user__last_name']

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "user"   :
            # way1 , it is not applicable because  we can not select the same user on edit mode to submit,
            # as a result you need to always change to the new user that it is impossible
            managers = list(Manager.objects.values())
            list_manger_user_id = [x['user_id'] for x in managers]
            list_manger_user_id.append(1)  # always being admin

            engineers = list(Engineer.objects.values())
            list_engineer_user_id = [x['user_id'] for x in engineers]

            kwargs["queryset"] =User.objects.filter(~Q(id__in=list_manger_user_id),~Q(id__in=list_engineer_user_id),is_active=True)

            # way2 , already added user keep listing on dropdownlist but we can prevent duplicate manager by setting unique value
            # kwargs["queryset"] = User.objects.filter( is_active=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["user"]
        else:
            return []



@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    actions = None
    model=Branch
    list_display = ['branch_name', 'company']
    search_fields = ['branch_name','company__company_name']
    list_filter=(CompanyFilter,)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            kwargs["queryset"] =Company.objects.filter(is_customer=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(DataCenter)
class DataCenterAdmin(admin.ModelAdmin):
    actions = None
    model=DataCenter
    list_display = ['datacenter_name', 'company']
    search_fields = ['datacenter_name','company__company_name']
    list_filter=(CompanyFilter,)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            kwargs["queryset"] =Company.objects.filter(is_customer=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    actions = None
    model=Customer
    list_display = ['company','customer_name','is_active']
    list_filter=(CompanyFilter,)
    search_fields = ['customer_name','company__company_name']
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "company":
            kwargs["queryset"] =Company.objects.filter(is_customer=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    model=Product
    actions = None
    list_display = ['product_name','partner_company','customer_company','is_active']
    search_fields = ['product_name','partner_company__company_name','customer_company__company_name']
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "partner_company":
            kwargs["queryset"] =Company.objects.filter(is_subcontractor=True)
        if db_field.name == "customer_company":
            kwargs["queryset"] =Company.objects.filter(is_customer=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    actions = None
    list_display=['enq_id','project_name','company']
    search_fields=['enq_id','project_name','company__company_name']


@admin.register(Product_Type)
class Product_TypeAdmin(admin.ModelAdmin):
    actions = None
    model=Product_Type
    list_display = ['productype_name']
    search_fields = ['productype_name']

@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    actions = None
    model=Brand
    list_display = ['brand_name']
    search_fields = ['brand_name']

@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    actions = None
    model=Model
    list_display = ['model_name', 'brand','is_active','model_updated_at']
    search_fields = ['model_name','brand__brand_name']
    list_filter=(BrandFilter,)


@admin.register(Function)
class FunctionAdmin(admin.ModelAdmin):
    actions = None
    model=Function
    list_display = ['function_name']
    search_fields = ['function_name']


@admin.register(ServiceTeam)
class ServiceTeamAdmin(admin.ModelAdmin):
    actions = None
    model=ServiceTeam
    list_display = ['service_team_name', 'company']
    search_fields = ['service_team_name','company__company_name']
    list_filter=(CompanyFilter,)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # yit only ID=1
        if db_field.name == "company":
            kwargs["queryset"] =Company.objects.filter(is_subcontractor__exact=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    actions = None
    model=Employee
    list_display = ['employee_name','is_inactive','is_team_lead', 'employee_nickname','employee_email']
    search_fields = ['employee_name', 'employee_nickname']
    list_filter = ("is_inactive","is_team_lead",)

@admin.register(Incident_Severity)
class  Incident_SeverityAdmin(admin.ModelAdmin):
   actions = None
   readonly_fields = ('severity_level',)
   def has_delete_permission(self, request, obj=None):
       return False

@admin.register(Incident_Status)
class  Incident_StatusAdmin(admin.ModelAdmin):
   actions = None
   def has_delete_permission(self, request, obj=None):
       return False

   def has_change_permission(self, request, obj=None):
       return False
   def has_add_permission(self, request, obj=None):
       return False

@admin.register(Incident_Type)
class  Incident_TypeAdmin(admin.ModelAdmin):
   actions = None
   def has_delete_permission(self, request, obj=None):
       return False


@admin.register(Service_Type)
class  Service_TypeAdmin(admin.ModelAdmin):
   actions = None
   def has_delete_permission(self, request, obj=None):
       return False

@admin.register(SLA)
class  SLAAdmin(admin.ModelAdmin):
   actions = None
   def has_delete_permission(self, request, obj=None):
       return False


admin.site.register(Inventory)
admin.site.register(Incident)


class MyAdminModel(HistoryAdmin):
    history_latest_first = False    # latest changes first
    inline_models_history = '__all__'   # __all__ or list of inline models for this ModelAdmin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

UserAdmin.list_display = ( 'first_name', 'last_name', 'username','is_active')
UserAdmin.ordering = ( '-is_active','first_name','last_name')
UserAdmin.search_fields= ( 'first_name','last_name','username')
UserAdmin.actions=None

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    model=LogEntry
    list_display =   list_display = ('__str__', 'action_time')



@admin.register(ReportKeyValueWeight)
class ReportKeyValueWeightAdmin(admin.ModelAdmin):
    list_display=['key','name','weight_value','level1','level2','level3','level4','level5','is_used','updated_at']
    list_display_links = ['key']
    actions =None
    search_fields = ['key','name']
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["key"]
        else:
            return []
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(ReportLevelDefinition)
class ReportLevelDefinitionAdmin(admin.ModelAdmin):
    list_display=['key','name','level_value']
    list_display_links = ['key']
    actions =None
    search_fields = ['name']
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ["key"]
        else:
            return []
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(PreventiveMaintenance)
class PreventiveMaintenanceAdmin(admin.ModelAdmin):
    model = PreventiveMaintenance
@admin.register(PM_Inventory)
class PM_InventoryAdmin(admin.ModelAdmin):
    model=PM_Inventory


class PM_Inventory_TemplateForm(forms.ModelForm):
   class Meta:
        model = PM_Inventory_Template
        fields = "__all__"
   def clean_template_file_name(self):
     try:
         file_name=self.cleaned_data["template_file_name"]
         template_path=os.path.join(settings.STATIC_ROOT,settings.PM_PHYSICAL_TEMPLATE_PATH,file_name)
         if os.path.exists(template_path)==True:
             return  file_name
         else:
             raise Exception(f"not found template {template_path} on server. Contact administrator to upload template prior to adding data.")
     except Exception as ex:
         raise forms.ValidationError(ex)

@admin.register(PM_Inventory_Template)
class PM_Inventory_TemplateAdmin(admin.ModelAdmin):
    form=PM_Inventory_TemplateForm
    list_display=['template_file_name']
    actions = None
    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(TaskSchedule_PMDoc)
class TaskSchedule_PMDocAdmin(admin.ModelAdmin):
    actions = None
    list_display = ['id','file_name','pm_id','owner','created_date','complete_date','status']
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    # def has_change_permission(self, request, obj=None):
    #     return  False


@admin.register(Incident_Summary)
class Incident_SummaryAdmin(admin.ModelAdmin):

    list_display = ['incident','model','incident_updated_at','updated_at']
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return  False

@admin.register(Incident_Summary_UserFeedback)
class Incident_Summary_UserFeedbackAdmin(admin.ModelAdmin):

    list_display = ['id','incident_summary','satisfactory','updated_at']
    def has_delete_permission(self, request, obj=None):
        return False
    def has_add_permission(self, request, obj=None):
        return False
    def has_change_permission(self, request, obj=None):
        return  False

