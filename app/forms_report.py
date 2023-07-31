from django import forms
import app.utility as util


class ReportDateSearchForm(forms.Form):

    year_list = forms.ChoiceField(choices=util.list_year_selection(),label="Select Year" ,)
    quarter_list = forms.ChoiceField(choices=util.list_quarter_selection(),label="Select Period")

class AdvancedReportSearchForm(forms.Form):
    cust_comp_list = forms.ChoiceField(label="Customer-Company")
    start_date = forms.DateField(label="Issue Start-From",widget=forms.DateInput(attrs={'type':'date'}))
    end_date = forms.DateField(label="End-To",widget=forms.DateInput(attrs={'type':'date'}))

    def __init__(self, _current_user, *args, **kwargs):
    #def __init__(self, *args, **kwargs):
        super(AdvancedReportSearchForm, self).__init__(*args, **kwargs)
        self.current_user=_current_user
        list_cust_comp=util.list_customer_company(self.current_user)
        self.fields['cust_comp_list'].choices = list_cust_comp

