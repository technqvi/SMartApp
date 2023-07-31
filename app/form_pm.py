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
        }

    def __init__(self, *args, **kwargs):
        super(PM_MasterForm, self).__init__(*args, **kwargs)
        self.fields['team_lead'].queryset =Employee.objects.filter(is_inactive=False).order_by('-is_team_lead','employee_name')
        self.fields['engineer'].queryset = Employee.objects.filter(is_inactive=False).order_by('employee_name')


class  PM_InventoryForm(forms.ModelForm):
    class Meta:
        model= PM_Inventory
        exclude=['pm_master','inventory']
        widgets = {
        'actual_date': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
        'document_date': MyDateInput(format=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M"], ),
        'remark': forms.Textarea(attrs={'rows': 5, 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super(PM_InventoryForm, self).__init__(*args, **kwargs)
        self.fields['pm_engineer'].queryset =Employee.objects.filter(is_inactive=False)
        self.fields['document_engineer'].queryset =Employee.objects.filter(is_inactive=False)

