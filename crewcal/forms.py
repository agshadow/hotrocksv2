from django import forms
from crewcal.models import DateEntry, Job
from django.forms import DateInput

DateEntryForm = forms.modelform_factory(
    DateEntry,
    fields=[
        "date",
        "crew",
        "quantity",
        "notes",
    ],
)


DateEntryForm1 = forms.modelform_factory(
    DateEntry,
    fields=[
        "job",
        "date",
        "crew",
        "notes",
        "quantity",
    ],
    widgets={
        "date": DateInput(
            attrs={
                "type": "date",
            }
        )
    },
)


JobForm = forms.modelform_factory(
    Job,
    fields=[
        "name",
        "number",
        "location",
        "company_workgroup",
    ],
    widgets={"company_workgroup": forms.HiddenInput()},
)
JobForm.base_fields["number"].label = "Job Number"
