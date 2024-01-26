from django.test import TestCase
from datetime import date
from crewcal.models import (
    Job,
    DateEntry,
    UserProfile,
    Workgroup,
    CompanyWorkgroup,
    Company,
)
from django.contrib.auth.models import User


def setup_one_job(self):
    self.wg = Workgroup.objects.create(name="Melbourne")
    self.cp = Company.objects.create(name="Unisys")
    self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

    self.user = User.objects.create_superuser(
        username="admin", password="adminpass", email="admin@example.com"
    )
    self.userprofile = UserProfile.objects.create(
        user=self.user,
        company_workgroup=self.cw,
    )
    self.job = Job.objects.create(
        name="Hibiscus Stage 1",
        number="22-02-4423",
        location="Grange Road, Plumpton",
        company_workgroup=self.cw,
    )
    self.entry1 = DateEntry.objects.create(
        job=self.job,
        date=date(2024, 1, 8),
        crew="Jeff",
        notes="Prime and Sami",
        quantity="300T 10N",
    )
    self.entry2 = DateEntry.objects.create(
        job=self.job,
        date=date(2024, 1, 9),
        crew="Jeff",
        notes="Prime and Sami",
        quantity="300T 7N",
    )
    self.entry3 = DateEntry.objects.create(
        job=self.job,
        date=date(2024, 1, 10),
        crew="Jeff",
        notes="Prime and Sami",
        quantity="300T 20SI",
    )


class TestSetUpOneJob(TestCase):
    def setUp(self):
        setup_one_job(self)

    def test_should_have_create_test_data(self):
        self.assertEqual(DateEntry.objects.count(), 3)
        self.assertEqual(Job.objects.count(), 1)


def create_superuser_profile(self):
    # Create a superuser for logging into the admin site
    self.wg = Workgroup.objects.create(name="Melbourne")
    self.cp = Company.objects.create(name="Unisys")
    self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

    self.user = User.objects.create_superuser(
        username="admin", password="adminpass", email="admin@example.com"
    )
    self.userprofile = UserProfile.objects.create(
        user=self.user,
        company_workgroup=self.cw,
    )
