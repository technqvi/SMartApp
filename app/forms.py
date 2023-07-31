from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q

import datetime as datetime
#from django.forms import ModelForm
from django.forms import modelformset_factory
from django.forms import BaseModelFormSet
from django.conf import settings

import os

#from dal import autocomplete
# from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

def validate_start_to_date(cleaned_data,startDate_fieldName,endDate_fieldName):
  start_date=cleaned_data.get(startDate_fieldName)
  end_date=cleaned_data.get(endDate_fieldName)
  if (start_date is not None) and (end_date is not None):
      if start_date >  end_date:
       # raise ValidationError(_(f' {startDate_fieldName} must be less than {endDate_fieldName}'))
       return  _(f' {endDate_fieldName} must be more than {startDate_fieldName}')
  else:
      return None


class MyDateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)

class MyTimeInput(forms.TimeInput):
    input_type = "time"

class MyDateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    #input_type = "datetime"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%dT%H:%M"
        super().__init__(**kwargs)
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))


class ProjectForm(forms.ModelForm):
    class Meta:
        model=Project
        fields ='__all__'
        widgets = {
            'project_name': forms.TextInput(attrs={'size':100}),
            'project_start': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
            'project_end': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        year_enq=int(datetime.date.today().strftime('%y'))+43
        self.fields['enq_id'].initial = f"ENQ/{year_enq}-"

    def clean(self):
        cleaned_data = super().clean()
        error_project_date = validate_start_to_date(cleaned_data, "project_start", "project_end")
        if error_project_date is not None:
            self.add_error("project_start", ValidationError(error_project_date))

class InventoryForm(forms.ModelForm):
    class Meta:
        model=Inventory
        fields ='__all__'

        widgets = {
            # 'project':forms.TextInput(attrs={'readonly':'readonly'}),
            'project': forms.HiddenInput(),

            'customer_warranty_start': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
            'customer_warranty_end': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
            'yit_warranty_start':  MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
            'yit_warranty_end':  MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
            'product_warranty_start': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
            'product_warranty_end':  MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),

            'install_date':  MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
            'eos_date':  MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),

            'remark': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'part_detail': forms.Textarea(attrs={'rows': 10, 'class': 'form-control'}),
            # 'cm_serviceteam':autocomplete.ModelSelect2(url='add_inventory'),

        }

    def __init__(self, *args, **kwargs):
        super(InventoryForm, self).__init__(*args, **kwargs)

        self.fields['serial_number'].initial = settings.SERIAL_NO_DEFAULT

        self.fields['model'].queryset =Model.objects.none()
        if 'brand' in self.data:
            try:
             brand_idx=int(self.data.get('brand'))
             self.fields['model'].queryset = Model.objects.filter(brand_id=brand_idx).order_by('model_name')
            except(ValueError,TypeError):
                pass

        elif self.instance.id:
            self.fields['model'].queryset = self.instance.brand.model_set.order_by('model_name')

    
    def clean(self):
          cleaned_data = super().clean()

          self.validate_inventory_date(cleaned_data)

          inventory_id=self.instance.id
          serial_no = self.cleaned_data['serial_number']
          project = self.cleaned_data['project']
          x_product_type = self.cleaned_data['product_type']

          if Inventory.objects.filter(~Q(id = inventory_id),~Q(serial_number =settings.SERIAL_NO_DEFAULT),
                                      project_id=project.id,
                                      serial_number=serial_no,
                                      product_type_id=x_product_type.id).count() > 0:
              self.add_error("serial_number", ValidationError(_(
                 f'Not allow have more than one the same serial number {serial_no} in same ENQ as {project.enq_id} AND product type  {x_product_type.productype_name}')))

    # the same method in add_inventory and copy_inventory
    def validate_inventory_date(self, cleaned_data):
        error_cust_date = validate_start_to_date(cleaned_data, "customer_warranty_start", "customer_warranty_end")
        if error_cust_date is not None:
            self.add_error("customer_warranty_end", ValidationError(error_cust_date))
        error_yit_date = validate_start_to_date(cleaned_data, "yit_warranty_start", "yit_warranty_end")
        if error_yit_date is not None:
            self.add_error("yit_warranty_end", ValidationError(error_yit_date))
        error_product_date = validate_start_to_date(cleaned_data, "product_warranty_start", "product_warranty_end")
        if error_product_date is not None:
            self.add_error("product_warranty_end", ValidationError(error_product_date))
    def clean_serial_number(self):
        serial_number = self.cleaned_data['serial_number']
        return    serial_number.strip()


class InventoryForCopyForm(forms.ModelForm):
    # brand=forms.ModelChoiceField(queryset=Branch.objects.none(),disabled=True)
    # model = forms.ModelChoiceField(queryset=Model.objects.none(), disabled=True)
    class Meta:
     model = Inventory
     fields = ('id','serial_number','product_type','brand','model','quantity',
              'customer_warranty_start','customer_warranty_end','customer_sla',
              'yit_warranty_start', 'yit_warranty_end', 'yit_sla',
              'product_warranty_start', 'product_warranty_end', 'product_sla',
              # 'cm_serviceteam','pm_serviceteam',

              )

     widgets = {

         'id': forms.HiddenInput(),
        'serial_number':forms.TextInput(attrs={'readonly':'readonly','size': 20}),

        'customer_warranty_start': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
        'customer_warranty_end': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
        'yit_warranty_start': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
        'yit_warranty_end': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
        'product_warranty_start': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
        'product_warranty_end': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),

     }

     # def __init__(self, *args, **kwargs):
     #     super(InventoryForCopyForm, self).__init__(*args, **kwargs)

     def clean(self):
       cleaned_data = super().clean()
       self.validate_inventory_date(cleaned_data)

     def validate_inventory_date(self, cleaned_data):
         error_cust_date = validate_start_to_date(cleaned_data, "customer_warranty_start", "customer_warranty_end")
         if error_cust_date is not None:
             self.add_error("customer_warranty_end", ValidationError(error_cust_date))
         error_yit_date = validate_start_to_date(cleaned_data, "yit_warranty_start", "yit_warranty_end")
         if error_yit_date is not None:
             self.add_error("yit_warranty_end", ValidationError(error_yit_date))
         error_product_date = validate_start_to_date(cleaned_data, "product_warranty_start", "product_warranty_end")
         if error_product_date is not None:
             self.add_error("product_warranty_end", ValidationError(error_product_date))


InventoryFormset=modelformset_factory(Inventory,form= InventoryForCopyForm,exclude=('remark','project')
                                      ,extra=0,can_delete=True, can_order=True)



class IncidentForm(forms.ModelForm):
    class Meta:
        model = Incident
        exclude=['inventory','incident_no']
        #fields = '__all__'
        widgets = {
            'incident_datetime': MyDateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
            'incident_close_datetime': MyDateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
            'incident_problem_start': MyDateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
            'incident_problem_end': MyDateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
            'incident_description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
            'incident_subject': forms.Textarea(attrs={'rows': 1, 'class': 'form-control'}),
            # 'incident_description': forms.Textarea(attrs={'rows': 5, 'class': 'form-control', 'id': '#id_incident_description'}),
            'incident_customer_support': forms.Textarea(attrs={'rows': 2, 'class': 'form-control'}),

        }

    def __init__(self, *args, **kwargs):
        super(IncidentForm, self).__init__(*args, **kwargs)
        self.fields['incident_datetime'].initial = datetime.datetime.now()


    def clean(self):
             cleaned_data = super().clean()

             error1 = validate_start_to_date(cleaned_data, "incident_datetime", "incident_close_datetime")
             if error1 is not None:
                 self.add_error("incident_datetime", ValidationError(error1))
             error2 = validate_start_to_date(cleaned_data, "incident_problem_start", "incident_problem_end")
             if error2 is not None:
                 self.add_error("incident_problem_start", ValidationError(error2))

             error3 = validate_start_to_date(cleaned_data, "incident_datetime", "incident_problem_start")
             if error3 is not None:
                 self.add_error("incident_datetime", ValidationError(error3))

             error4 = validate_start_to_date(cleaned_data, "incident_problem_end", "incident_close_datetime")
             if error4 is not None:
                 self.add_error("incident_problem_end", ValidationError(error4))

             #error
             incident_status= cleaned_data.get("incident_status")
             incident_close_datetime = cleaned_data.get("incident_close_datetime")
             if incident_status.id== settings.INCIDENT_CODE_CLOSED and incident_close_datetime is None:
                 self.add_error("incident_status", f"You must always specify Incident-Closed-Date on {incident_status}")
             elif incident_status.id!= settings.INCIDENT_CODE_CLOSED and incident_close_datetime is not None:
                 self.add_error("incident_status", f"You are not allowed to specify Incident-Closed-Date on {incident_status} (reload page to clear close datetime)")



class IncidentFileForm(forms.ModelForm):
    class Meta:
        model = Incident_File
        fields ='__all__'
        widgets = {
            'incident_ref': forms.HiddenInput(),
            'incident_file':forms.ClearableFileInput(attrs={'multiple': False}),
        }

    def clean2(self,file):

        try:
            content_type = file.content_type
            if content_type in settings.UPLOAD_FILE_TYPES:
                content_size=file.size
                x=round((content_size/1024/1024),2)
                y= settings.UPLOAD_FILE_MAX_SIZE_MB
                xy=settings.UPLOAD_FILE_UNIT
                if x > y:
                    raise ValidationError((f'Your file size is {x} {xy} , file size must be less than {y} {xy}. ') )
            else:
                raise ValidationError((f'File type {content_type} is not supported to upload.'))
        except AttributeError:
            pass
    def clean(self):
     cleaned_data = super().clean()
     if self.cleaned_data.get("incident_file") is not None  :

         self.clean2(self.cleaned_data.get("incident_file"))

         x_file = self.cleaned_data.get("incident_file").name
         x_file=x_file.replace(' ','_')
         x_ref=self.cleaned_data.get("incident_ref")

         if x_ref is not None:
           x_incident_ref_id=self.cleaned_data.get("incident_ref").id
           x_path= f'{settings.MEDIA_ROOT}\\{settings.INCIDENT_PREFIX_DOC}{x_incident_ref_id}\\'
           #x_path= f'{settings.PRIVATE_STORAGE_ROOT}\\{settings.INCIDENT_PREFIX_DOC}{x_incident_ref_id}\\'
           if  os.path.exists(x_path): # check only already exiting folder for storing file
            file_path=x_path + x_file
            if os.path.exists(file_path):
              raise ValidationError(_(f'A file {x_file} already exists. Rename the file and upload it again.'))


   # check_fileType_limitSize


class  Incident_DetailForm(forms.ModelForm):
    class Meta:
        model= Incident_Detail
        #fields = '__all__'
        exclude=['incident_master']
        widgets = {
        'task_start': MyDateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"],),
        # 'task_start': AdminDateWidget(
        #          attrs={'class': 'picker',  'autocomplete': 'off'}),
        'task_end': MyDateTimeInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
        'workaround_resolution': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(Incident_DetailForm, self).__init__(*args, **kwargs)
        self.fields['employee'].queryset =Employee.objects.filter(is_inactive=False)

    def clean(self):
        cleaned_data = super().clean()

        error=validate_start_to_date(cleaned_data,"task_start","task_end")
        if error is not None:
            self.add_error("task_end", ValidationError(error))


Incident_DetailFormset=modelformset_factory(Incident_Detail,form= Incident_DetailForm,exclude=('incident_master',),extra=2)

class ExportBrandForm(forms.Form):
    brand_list=forms.ModelMultipleChoiceField(  label='Brand List',queryset=Brand.objects.all(),
                                                widget = forms.CheckboxSelectMultiple,required=True)
class UploadModelForm(forms.Form):
    template_file = forms.FileField(required=False)



class  CustomerForm(forms.ModelForm):
    class Meta:
        model= Customer
        fields = '__all__'
        # exclude=['company']
class  ProductForm(forms.ModelForm):
    class Meta:
        model= Product
        fields = '__all__'
        # exclude=['partner_company','customer_company']



# from django_cascading_dropdown_widget.widgets import DjangoCascadingDropdownWidget
# from django_cascading_dropdown_widget.widgets import CascadingModelchoices
#https://pypi.org/project/django-cascading-dropdown-widget/

def list_customer_by_customer(self):
        self.fields['customer'].queryset = Customer.objects.none()
        if 'customer' in self.data:
            try:
                company_idx = int(self.data.get('company'))
                self.fields['customer'].queryset = Customer.objects.filter(company_id=company_idx).order_by(
                    'customer_name')
            except(ValueError, TypeError):
                pass
        elif self.instance.id:
            self.fields['customer'].queryset = self.instance.company.customer_set.order_by('customer_name')
class BranchForm(forms.ModelForm):
    class Meta:
        model =Branch
        fields = '__all__'
        widget={
            'address': forms.Textarea(attrs={"rows": 5, "cols":10,"class": 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(BranchForm, self).__init__(*args, **kwargs)
        list_customer_by_customer(self)

class DataCenterForm(forms.ModelForm):
    class Meta:
        model =DataCenter
        fields = '__all__'
        widget={
            'address': forms.Textarea(attrs={"rows": 5, "cols":10,"class": 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(DataCenterForm, self).__init__(*args, **kwargs)
        list_customer_by_customer(self)



#https://djangotricks.blogspot.com/2019/10/working-with-dates-and-times-in-forms.html
#https://knews.vip/postcrawl/stack/view?site=so&key=74074486&lang=th&alias=django-form-dateinput-phrxm-wid-cet-ni-kar-xaphdet-kar-suy-seiy-kha-reim-tn

class XYZ_DateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        # kwargs["format"] = '%d/%m/%Y'
        super().__init__(**kwargs)

class XYZ_DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"
    def __init__(self, **kwargs):

        # kwargs["format"] = "%Y-%m-%dT%H:%M"
        kwargs["format"] = "%Y-%m-%d %H:%M"
        # kwargs["format"] = '%d/%m/%Y %H:%M'
        super().__init__(**kwargs)

# from datetimewidget.widgets import DateTimeWidget,DateWidget

# dateOptions = {
# 'format': 'dd/mm/yyyy',
# 'autoclose': True,
#
# }
# dateTimeOptions = {
# 'format': 'dd/mm/yyyy hh:ii',
# 'autoclose': True,
#
# }

class XYZ_TestDataForm(forms.ModelForm):
    class Meta:
        model =XYZ_TestData
        is_localized = True
        fields = '__all__'
        widgets = {
            'my_date': XYZ_DateInput(format=["%Y-%m-%d"], ),
            # 'my_date':XYZ_DateInput(format=['%d/%m/%Y'],),

            'my_date_time': XYZ_DateTimeInput(format=[ "%Y-%m-%d %H:%M"],),
            # 'my_date_time': XYZ_DateTimeInput(format=["%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"], ),
            # 'my_date_time': XYZ_DateTimeInput(format=['%d/%m/%Y %H:%M'], ),
            #
            # 'my_date': DateWidget(attrs={'id': '#id_my_date'}, bootstrap_version=3.4),
            # 'my_date_time': DateTimeWidget(attrs={'id': '#id_my_date_time'},bootstrap_version=3.4),

        }




class PMInventoryTemplateForm(forms.ModelForm):

    class Meta:
     model = PM_Inventory_Template
     fields = ('template_des','sample_part_detail')

     widgets = {
     'template_des': forms.TextInput(),
        'sample_part_detail': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),

     }

PMInventoryTemplateFormSet=modelformset_factory(PM_Inventory_Template,form= PMInventoryTemplateForm,exclude=('template_file_name',)
                                      ,extra=0,can_delete=False, can_order=True)