from django import forms
from report.models import IncidentReport, IncidentTypeChoice
from datetime import datetime, date

#IncidentReportForm = \
 #   forms.modelform_factory(IncidentReport, exclude=["sign_off",],queryset=IncidentReport.objects.all())
class DateTimeInput(forms.DateTimeInput):
    input_type = "datetime-local"

class IncidentReportForm(forms.ModelForm):
#class IncidentReportForm(TemplatedForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sign_off_date'].widget = forms.widgets.DateInput(
            attrs={
                'type': 'date', 'placeholder': 'yyyy-mm-dd (DOB)',
                'class': 'form-control'
                }
            )
        self.fields['incident_date'].widget = DateTimeInput()
        self.fields["witness_name"].label = "Wittness Name - enter a witness"
        self.fields["description"].help_text = "* required"

    class Meta:
        model = IncidentReport
        fields = '__all__'

    incident_type = forms.CharField(widget=forms.Select(choices = IncidentTypeChoice.choices))
    incident_date = forms.DateTimeField()
    site = forms.CharField()
    date_reported = forms.DateField(required=False)
    reported_by = forms.CharField()
    reported_to = forms.CharField(required=False)
    witness_name = forms.CharField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={"rows": "6", "cols": "50"}))
    root_cause = forms.CharField(widget=forms.Textarea(attrs={"rows": "6", "cols": "50"}),required=False)
    action_taken = forms.CharField(widget=forms.Textarea(attrs={"rows": "6", "cols": "50"}),required=False)
    sign_off = forms.CharField()
    sign_off_date = forms.DateField()