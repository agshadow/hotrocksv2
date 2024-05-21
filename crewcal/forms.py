from django import forms
from crewcal.models import DateEntry, Job, UserProfile
from django.forms import DateInput
from datetime import date, timedelta

DateEntryForm = forms.modelform_factory(
    DateEntry,
    fields=[
        "date",
        "crew",
        "quantity",
        "notes",
    ],
    widgets={
        "date": DateInput(
            attrs={
                "type": "date",
            }
        )
    },
)


class DateEntryForm1(forms.ModelForm):
    days = forms.IntegerField(min_value=1, label="Days")

    class Meta:
        model = DateEntry
        fields = ["job", "date", "crew", "notes", "quantity"]
        widgets = {
            "date": DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super(DateEntryForm1, self).__init__(*args, **kwargs)
        if self.user:
            try:
                user_profile = UserProfile.objects.get(user=self.user)
                company_workgroup = user_profile.company_workgroup
                self.fields["job"].queryset = Job.objects.filter(
                    company_workgroup=company_workgroup
                )
            except UserProfile.DoesNotExist:
                self.fields["job"].queryset = Job.objects.none()

    def save_multiple_entries(self):
        job = self.cleaned_data["job"]
        date = self.cleaned_data["date"]
        days = self.cleaned_data["days"]
        crew = self.cleaned_data["crew"]
        notes = self.cleaned_data["notes"]
        quantity = self.cleaned_data["quantity"]

        entries = []
        for i in range(days):
            entry = DateEntry(
                job=job,
                date=date + timedelta(days=i),
                crew=crew,
                notes=notes,
                quantity=quantity,
            )
            entries.append(entry)

        DateEntry.objects.bulk_create(entries)


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


class DateEntryForm2(forms.ModelForm):
    """search_job = forms.CharField(
        required=False,
        label="Search Jobs",
        widget=forms.TextInput(attrs={"placeholder": "Search jobs1..."}),
    )"""

    class Meta:
        model = DateEntry
        fields = ["job", "date", "crew", "notes", "quantity"]

    def __init__(self, user, *args, **kwargs):
        super(DateEntryForm2, self).__init__(*args, **kwargs)
        # Filter jobs based on the user's customer_workgroup
        self.fields["job"].queryset = Job.objects.filter(
            company_workgroup=user.userprofile.company_workgroup
        )
