from django import forms
from crewcal.models import DateEntry

DateEntryForm = forms.modelform_factory(
    DateEntry, 
    fields=["date", "crew", "quantity", "notes",],
    )