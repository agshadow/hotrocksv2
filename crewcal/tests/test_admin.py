from django.test import TestCase
from crewcal.models import (
    Job,
    DateEntry,
)
import crewcal.tests.test_setup as test_setup


class TestJobAdmin(TestCase):
    def setUp(self):
        test_setup.create_superuser_profile(self)
        # Create a sample job for testing
        self.job = Job.objects.create(
            name="Software Developer",
            number="JD123",
            location="Cityville",
            company_workgroup=self.cw,
        )

        self.date_entry = DateEntry.objects.create(
            job=self.job,
            date="2022-01-15",
            crew="Dev Team",
            notes="Project meeting",
            quantity="10",
        )

    def test_job_displayed_in_admin(self):
        # Log in the admin user
        self.client.login(username="admin", password="adminpass")

        # Get the change page for the Job model
        change_page_url = f"/admin/crewcal/job/{self.job.id}/change/"

        # Issue a GET request to the change page
        response = self.client.get(change_page_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.name)

    def test_job_displayed_in_admin_list(self):
        # Log in the admin user
        self.client.login(username="admin", password="adminpass")

        # Get the change page for the Job model
        change_page_url = "/admin/crewcal/job/"

        # Issue a GET request to the change page
        response = self.client.get(change_page_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the job's name is displayed in the list view
        self.assertContains(response, "Software Developer")

    def test_job_search_in_admin(self):
        # Log in the admin user
        self.client.login(username="admin", password="adminpass")

        # Get the search page for the Job model
        search_url = "/admin/crewcal/job/?q=Software"

        # Issue a GET request to the search page
        response = self.client.get(search_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the job's name is found in the search results
        self.assertContains(response, "Software Developer")

    def test_dates_for_job_in_job_admin_screen(self):
        self.client.login(username="admin", password="adminpass")

        # Get the change page for the Job model
        change_page_url = "/admin/crewcal/job/"

        # Issue a GET request to the change page
        response = self.client.get(change_page_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the job's name is displayed in the list view
        self.assertContains(response, "Associated Dates")
        self.assertContains(response, "Date Entries")


class TestDateEntryAdmin(TestCase):
    def setUp(self):
        test_setup.create_superuser_profile(self)
        # Create a sample Job for testing
        self.job = Job.objects.create(
            name="Software Developer",
            number="JD123",
            location="Cityville",
            company_workgroup=self.cw,
        )

        # Create a sample DateEntry for testing
        self.date_entry = DateEntry.objects.create(
            job=self.job,
            date="2022-01-15",
            crew="Dev Team",
            notes="Project meeting",
            quantity="10",
        )

    def test_date_entry_displayed_in_admin_list(self):
        # Log in the admin user
        self.client.login(username="admin", password="adminpass")

        # Get the change page for the DateEntry model
        change_page_url = "/admin/crewcal/dateentry/"

        # Issue a GET request to the change page
        response = self.client.get(change_page_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the date entry's date is displayed in the list view
        self.assertContains(response, "Jan. 15, 2022")

    def test_date_entry_search_in_admin(self):
        # Log in the admin user
        self.client.login(username="admin", password="adminpass")

        # Get the search page for the DateEntry model
        search_url = "/admin/crewcal/dateentry/?q=Dev"

        # Issue a GET request to the search page
        response = self.client.get(search_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the date entry's crew is found in the search results
        self.assertContains(response, "Dev Team")
