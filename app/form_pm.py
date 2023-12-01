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
       # raise ValidationError(_(f' {startDate_fieldName} must be less than {endDate_fieldName}'))
       return  _(f' {endDate_fieldName} must be more than {startDate_fieldName}')
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
        exclude = ['project']
        widgets = {
            'remark': forms.TextInput(attrs={'size': 150}),
            'planned_date': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
            'ended_pm_date' : MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
        }

    def clean(self):
        cleaned_data = super().clean()
        error_project_date = validate_start_to_date(cleaned_data, "planned_date", "ended_pm_date")
        if error_project_date is not None:
            self.add_error("planned_date", ValidationError(error_project_date))

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

