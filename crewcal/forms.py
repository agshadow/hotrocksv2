from django import forms
from crewcal.models import DateEntry, Job, UserProfile
from django.forms import DateInput

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
    class Meta:
        model = DateEntry
        fields = ["job", "date", "crew", "notes", "quantity"]
        widgets = {
            "date": DateInput(attrs={"type": "date"}),
        }

    def __init__(self, *args, **kwargs):
        print("in dateEntryForm1.__init__ ")
        user = kwargs.pop("user", None)
        super(DateEntryForm1, self).__init__(*args, **kwargs)
        if user:
            print("in if uer")
            try:
                user_profile = UserProfile.objects.get(user=user)
                print(user_profile)
                company_workgroup = user_profile.company_workgroup
                print(company_workgroup)
                self.fields["job"].queryset = Job.objects.filter(
                    company_workgroup=company_workgroup
                )
            except UserProfile.DoesNotExist:
                self.fields["job"].queryset = Job.objects.none()
        else:
            print("in if-user-else statement")


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
