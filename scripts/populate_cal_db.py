from datetime import date

from django.contrib.auth.models import User

from crewcal.models import Job, DateEntry, UserProfile, Workgroup, Company, CompanyWorkgroup


wg = Workgroup.objects.create(name="Melbourne")
cp = Company.objects.create(name="Unisys")
cw = CompanyWorkgroup.objects.create(company=cp, workgroup=wg)

wg1 = Workgroup.objects.create(name="Sydney")
cp1 = Company.objects.create(name="Accenture")
cw1 = CompanyWorkgroup.objects.create(company=cp1, workgroup=wg1)

user = User.objects.create_user(username='accentureuser', password='adminpass', email='admin@example.com')
 
userprofile = UserProfile.objects.create(
    user = user,
    company_workgroup = cw1,
        )



job = Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton",
            company_workgroup = cw
        )
entry1 = DateEntry.objects.create(
            job = job,
            date = date(2024, 1, 8),
            crew = "Jeff",
            notes = "Prime and Sami",
            quantity = "300T 10N",
        )
entry2 = DateEntry.objects.create(
    job = job,
    date = date(2024,1,9),
    crew = "Jeff",
    notes = "Prime and Sami",
    quantity = "300T 7N",
)
entry3 = DateEntry.objects.create(
    job = job,
    date = date(2024,1,10),
    crew = "Jeff",
    notes = "Prime and Sami",
    quantity = "300T 20SI",
)
job1 = Job.objects.create(
            name = "Bridgefield Stage 1",
            number = "22-02-3152",
            location = "Greigs Rd Rockbank",
            company_workgroup = cw1,
        )
entry1_1 = DateEntry.objects.create(
            job = job1,
            date = date(2024, 1, 8),
            crew = "Lee",
            notes = "Prime and Sami",
            quantity = "100T 10N",
        )
job2 = Job.objects.create(
            name = "Highett Station",
            number = "22-02-4555",
            location = "Highett Road Highett Station",
            company_workgroup = cw
        )
entry2_1 = DateEntry.objects.create(
            job = job2,
            date = date(2024, 1, 9),
            crew = "Plugga",
            notes = "Prime and Sami",
            quantity = "500T 20SI",
        )
entry2_1 = DateEntry.objects.create(
            job = job2,
            date = date(2024, 1, 10),
            crew = "Plugga",
            notes = "Prime and Sami",
            quantity = "500T 20SI",
        )