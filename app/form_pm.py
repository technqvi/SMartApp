from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.core.exceptions import ValidationError
from django.db.models import Q

import datetime as datetime
from django.forms import ModelForm
from django.forms import modelformset_factory
from django.forms import BaseModelFormSet
from django.conf import settings

def validate_start_to_date(cleaned_data,startDate_fieldName,endDate_fieldName):
  start_date=cleaned_data.get(startDate_fieldName)
  end_date=cleaned_data.get(endDate_fieldName)
  if (start_date is not None) and (end_date is not None):
      if start_date >  end_date:
       return  _(f'{endDate_fieldName} must be greater or equal {startDate_fieldName}')
  else:
      return None

class MyDateInput(forms.DateInput):
    input_type = "date"
    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)



class  PM_MasterForm(forms.ModelForm):
    class Meta:
        model= PreventiveMaintenance
        exclude=['project']
        # fields ='__all__'
        widgets = {
            'remark': forms.TextInput(attrs={'size': 150}),
            'planned_date': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
            'ended_pm_date' : MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
            'postponed_date': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),

        }

    def clean(self):
        cleaned_data = super().clean()
        # validate#1
        error_planed_date = validate_start_to_date(cleaned_data, "planned_date", "ended_pm_date")
        if error_planed_date is not None:
            self.add_error("planned_date", ValidationError(error_planed_date))

        # # validate#2
        if self.instance.id is not None:
            pm=self.instance
            project=pm.project

            start_project=project.project_start
            end_project=project.project_end
            planned_date=self.cleaned_data['planned_date']
            if planned_date<start_project or planned_date>end_project:
                self.add_error("planned_date", f"planned_date:{planned_date} must be between project start:{start_project} and project-end:{end_project}")

            ended_pm_date=self.cleaned_data['ended_pm_date']
            if ended_pm_date<start_project or ended_pm_date>end_project:
                self.add_error("ended_pm_date", f"ended_pm_date:{ended_pm_date} must be between project start:{start_project} and project-end:{end_project}")


    # def __init__(self, *args, **kwargs):
    #     super(PM_MasterForm, self).__init__(*args, **kwargs)
    #     self.fields['team_lead'].queryset =Employee.objects.filter(is_inactive=False).order_by('-is_team_lead','employee_name')
    #     self.fields['engineer'].queryset = Employee.objects.filter(is_inactive=False).order_by('employee_name')


class  PM_InventoryForm(forms.ModelForm):
    class Meta:
        model= PM_Inventory
        exclude=['pm_master','inventory']
        widgets = {
        'actual_date': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
        'document_date': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
        'remark': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
    # def __init__(self, *args, **kwargs):
    #     super(PM_InventoryForm, self).__init__(*args, **kwargs)
    #     self.fields['pm_engineer'].queryset =Employee.objects.filter(is_inactive=False)
    #     self.fields['document_engineer'].queryset =Employee.objects.filter(is_inactive=False)

    def clean(self):

       cleaned_data = super().clean()

      # Update Individual Item by PmItem ID (It can be used for all update /update by brand)
      #  if self.instance.id is not None:
      #       pm_item=self.instance
      #       planned_date=pm_item.pm_master.planned_date
      #       actual_date = self.cleaned_data['actual_date']
      #       if actual_date is not None:
      #         if  actual_date < planned_date:
      #           self.add_error("actual_date", f"actual_date:{actual_date} must be greater than or equal planed date:{planned_date}")
      #       document_date = self.cleaned_data['document_date']
      #       if document_date is not None:
      #         if  document_date < planned_date:
      #           self.add_error("document_date", f"document_date:{document_date} must be greater than or equal planed date :{planned_date}")

       error_actual_date = validate_start_to_date(cleaned_data, "actual_date", "document_date")
       if error_actual_date is not None:
            self.add_error("actual_date", ValidationError(error_actual_date))



