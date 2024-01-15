from datetime import date

from crewcal.models import Job, DateEntry, UserProfile, Workgroup, Company, CompanyWorkgroup

wg = Workgroup.objects.create(name="Melbourne")
wg1 = Workgroup.objects.create(name="Sydney")
cp = Company.objects.create(name="Unisys")
cp1 = Company.objects.create(name="Accenture")

job = Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton"
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