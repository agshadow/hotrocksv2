from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from django.urls import reverse

from datetime import date

from crewcal.utils import transpose_dates, get_calendar_for_date_range, start_of_week
from crewcal.models import (
    Job,
    DateEntry,
    UserProfile,
    Workgroup,
    CompanyWorkgroup,
    Company,
)


class TestTransposeDates(TestCase):
    def test_should_return_dates_formatted_correctly(self):
        transposed_format_required = {
            "0": "",
            "1": "Mon, Jan 8",
            "2": "Tue, Jan 9",
            "3": "Wed, Jan 10",
            "4": "Thu, Jan 11",
            "5": "Fri, Jan 12",
            "6": "Sat, Jan 13",
            "7": "Sun, Jan 14",
        }
        datefrom = date(2024, 1, 8)
        transposed = transpose_dates(datefrom)
        self.assertEqual(transposed, transposed_format_required)
        self.assertTrue("0" in transposed)

    def test_should_return_todays_date_if_not_specified(self):
        transposed = transpose_dates()
        self.assertTrue("0" in transposed)
        self.assertEqual(
            date.today().strftime("%a, %b %d").replace(" 0", " "), transposed["1"]
        )


class TestGetCalendarForWeek(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)
        self.user = User.objects.create_user(
            username="unisysuser",
            password="adminpass",
            email="admin@example.com",
        )
        self.userprofile = UserProfile.objects.create(
            user=self.user,
            company_workgroup=self.cw,
        )
        self.wg1 = Workgroup.objects.create(name="Sydney")
        self.cp1 = Company.objects.create(name="Accenture")
        self.cw1 = CompanyWorkgroup.objects.create(company=self.cp1, workgroup=self.wg1)

        self.user1 = User.objects.create_user(
            username="accentureuser", password="adminpass", email="admin@example.com"
        )

        UserProfile.objects.create(
            user=self.user1,
            company_workgroup=self.cw1,
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
        self.job1 = Job.objects.create(
            name="Bridgefield Stage 1",
            number="22-02-3152",
            location="Greigs Rd Rockbank",
            company_workgroup=self.cw1,
        )
        self.entry1_1 = DateEntry.objects.create(
            job=self.job1,
            date=date(2024, 1, 8),
            crew="Lee",
            notes="Prime and Sami",
            quantity="100T 10N",
        )
        self.job2 = Job.objects.create(
            name="Highett Station",
            number="22-02-4555",
            location="Highett Road Highett Station",
            company_workgroup=self.cw,
        )
        self.entry2_1 = DateEntry.objects.create(
            job=self.job2,
            date=date(2024, 1, 9),
            crew="Plugga",
            notes="Prime and Sami",
            quantity="500T 20SI",
        )
        self.entry2_1 = DateEntry.objects.create(
            job=self.job2,
            date=date(2024, 1, 10),
            crew="Plugga",
            notes="Prime and Sami",
            quantity="500T 20SI",
        )

    def test_should_return_jobs_formatted_per_crew(self):
        self.client.login(username="unisysuser", password="adminpass")

        url = "/cal/?datefrom=20240108&dateto=20240114"
        datefrom = date(2024, 1, 8)
        dateto = date(2024, 1, 14)
        self.client.get(url)
        url = reverse("cal_home")
        request = self.factory.get(url)
        request.user = self.user

        formatted_data = get_calendar_for_date_range(request, datefrom, dateto)
        self.assertTrue("0" in formatted_data)
        self.assertTrue("1" in formatted_data["0"])
        self.assertTrue("7" in formatted_data["0"])
        self.assertIn("Jeff", formatted_data["0"]["0"])


class TestStartOfWeek(TestCase):
    def test_should_return_start_of_the_week(self):
        date_to_submit = date(2024, 1, 24)
        self.assertEqual(date(2024, 1, 21), start_of_week(date_to_submit))
