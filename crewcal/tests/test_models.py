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


class TestJobModel(TestCase):
    def setUp(self):
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

    def test_should_be_able_to_create_a_job_model(self):
        jobs = Job.objects.count()
        self.assertEqual(jobs, 0)

    def test_should_be_able_to_add_a_job_to_database(self):
        Job.objects.create(
            name="Hibiscus Stage 1",
            number="22-02-4423",
            location="Grange Road, Plumpton",
            company_workgroup=self.cw,
        )
        jobs = Job.objects.count()
        self.assertEqual(jobs, 1)
        job = Job.objects.first()
        self.assertEqual(job.name, "Hibiscus Stage 1")
        self.assertEqual(job.number, "22-02-4423")
        self.assertEqual(job.location, "Grange Road, Plumpton")

    def test_should_display_job_as_str(self):
        job = Job.objects.create(
            name="Hibiscus Stage 1",
            number="22-02-4423",
            location="Grange Road, Plumpton",
            company_workgroup=self.cw,
        )
        self.assertIn("Hibiscus", str(job))
        self.assertIn("22-02-4423", str(job))
        self.assertIn("Grange Road, Plumpton", str(job))


class TestDateEntryModel(TestCase):
    def setUp(self):
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.job = Job.objects.create(
            name="Hibiscus Stage 1",
            number="22-02-4423",
            location="Grange Road, Plumpton",
            company_workgroup=self.cw,
        )

    def test_should_be_able_to_create_a_date_entry_model(self):
        jobs = DateEntry.objects.count()
        self.assertEqual(jobs, 0)

    def test_should_be_able_to_add_a_date_entry_to_database(self):
        entry = DateEntry.objects.create(
            job=self.job,
            date=date(2023, 1, 2),
            crew="Jeff",
            notes="Prime and Sami",
            quantity="300T 10N",
        )
        entry_count = DateEntry.objects.count()
        self.assertEqual(entry_count, 1)
        entry1 = DateEntry.objects.first()
        self.assertEqual(entry1.job, self.job)
        self.assertEqual(entry1.date, date(2023, 1, 2))
        self.assertEqual(entry1.crew, entry.crew)
        self.assertEqual(entry1.notes, entry.notes)
        self.assertEqual(entry1.quantity, entry.quantity)

    def test_should_display_date_entry_as_str(self):
        entry = DateEntry.objects.create(
            job=self.job,
            date=date(2023, 1, 2),
            crew="Jeff",
            notes="Prime and Sami",
            quantity="300T 10N",
        )
        self.assertIn("Hibiscus", str(entry))
        self.assertIn("2023-01-02", str(entry))
        self.assertIn("Jeff", str(entry))


class TestUserProfileModel(TestCase):
    def setUp(self):
        pass

    def test_should_be_able_to_create_a_date_entry_model(self):
        users = UserProfile.objects.count()
        self.assertEqual(users, 0)

    def test_should_be_able_to_add_a_company_and_workgroup(self):
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
        users = UserProfile.objects.count()
        self.assertEqual(users, 1)
        user = UserProfile.objects.first()
        self.assertEqual(user.company_workgroup, self.cw)

    def test_should_display_user_profile_in_admin_user_change_screen(self):
        # tests the Stacked Inline and UserAdmin Classes
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
        self.client.login(username="admin", password="adminpass")

        change_page_url = "/admin/auth/user/1/change/"
        response = self.client.get(change_page_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "User Profile")
        self.assertContains(response, "Company")
