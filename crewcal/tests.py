from django.test import TestCase
from datetime import date
from .models import Job, DateEntry
from django.contrib.auth.models import User

class TestHome(TestCase):       
    def setUp(self):
        self.job = Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton"
        )
        self.entry1 = DateEntry.objects.create(
            job = self.job,
            date = date(2024, 1, 8),
            crew = "Jeff",
            notes = "Prime and Sami",
            quantity = "300T 10N",
        )
        self.entry2 = DateEntry.objects.create(
            job = self.job,
            date = date(2024,1,9),
            crew = "Jeff",
            notes = "Prime and Sami",
            quantity = "300T 7N",
        )
        self.entry3 = DateEntry.objects.create(
            job = self.job,
            date = date(2024,1,10),
            crew = "Jeff",
            notes = "Prime and Sami",
            quantity = "300T 20SI",
        )
    def test_should_be_able_render_cal_page(self):
        url = "/cal/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)

    def test_should_display_calendar_for_week(self):
        url = "/cal/?datefrom=20240108&dateto=20240114"
        response = self.client.get(url)
        self.assertContains(response, "Mon, Jan 8")
        self.assertNotContains(response, "Mon, Jan 15")
        self.assertContains(response, "Sun, Jan 14")

    def test_should_be_able_render_cal_page_with_jobs_for_those_dates(self):
        url = "/cal/?datefrom=20240108&dateto=20240114"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertContains(response, "Jeff")

class TestJobModel(TestCase):
    def test_should_be_able_to_create_a_job_model(self):
        jobs = Job.objects.count()
        self.assertEqual(jobs, 0)

    def test_should_be_able_to_add_a_job_to_database(self):
        Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton"
        )
        jobs = Job.objects.count()
        self.assertEqual(jobs, 1)
        job = Job.objects.first()
        self.assertEqual(job.name,"Hibiscus Stage 1")
        self.assertEqual(job.number, "22-02-4423")
        self.assertEqual(job.location, "Grange Road, Plumpton")
    
    def test_should_display_job_as_str(self):
        job = Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton"
        )
        self.assertIn("Hibiscus",str(job))
        self.assertIn("22-02-4423",str(job))
        self.assertIn("Grange Road, Plumpton",str(job))


class TestDateEntryModel(TestCase):
    def setUp(self):
        self.job = Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton"
        )
    def test_should_be_able_to_create_a_date_entry_model(self):
        jobs = DateEntry.objects.count()
        self.assertEqual(jobs, 0)

    def test_should_be_able_to_add_a_date_entry_to_database(self):
        entry = DateEntry.objects.create(
            job = self.job,
            date = date(2023, 1, 2),
            crew = "Jeff",
            notes = "Prime and Sami",
            quantity = "300T 10N",
        )
        entry_count = DateEntry.objects.count()
        self.assertEqual(entry_count, 1)
        entry1 = DateEntry.objects.first()
        self.assertEqual(entry1.job,self.job)
        self.assertEqual(entry1.date, date(2023, 1, 2))
        self.assertEqual(entry1.crew, entry.crew)
        self.assertEqual(entry1.notes, entry.notes)
        self.assertEqual(entry1.quantity, entry.quantity)
    
    def test_should_display_date_entry_as_str(self):
     
        entry = DateEntry.objects.create(
            job = self.job,
            date = date(2023, 1, 2),
            crew = "Jeff",
            notes = "Prime and Sami",
            quantity = "300T 10N",
        )
        self.assertIn("Hibiscus",str(entry))
        self.assertIn("2023-01-02",str(entry))
        self.assertIn("Jeff",str(entry))


class TestJobAdmin(TestCase):
    def setUp(self):
        # Create a superuser for logging into the admin site
        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

        # Create a sample job for testing
        self.job = Job.objects.create(name='Software Developer', number='JD123', location='Cityville')


        self.date_entry = DateEntry.objects.create(
            job=self.job,
            date='2022-01-15',
            crew='Dev Team',
            notes='Project meeting',
            quantity='10'
        )

    def test_job_displayed_in_admin(self):
        # Log in the admin user
        self.client.login(username='admin', password='adminpass')

        # Get the change page for the Job model
        change_page_url = f'/admin/crewcal/job/{self.job.id}/change/'

        # Issue a GET request to the change page
        response = self.client.get(change_page_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.job.name)


    def test_job_displayed_in_admin_list(self):
        # Log in the admin user
        self.client.login(username='admin', password='adminpass')

        # Get the change page for the Job model
        change_page_url = '/admin/crewcal/job/'

        # Issue a GET request to the change page
        response = self.client.get(change_page_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the job's name is displayed in the list view
        self.assertContains(response, 'Software Developer')

    def test_job_search_in_admin(self):
        # Log in the admin user
        self.client.login(username='admin', password='adminpass')

        # Get the search page for the Job model
        search_url = f'/admin/crewcal/job/?q=Software'

        # Issue a GET request to the search page
        response = self.client.get(search_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the job's name is found in the search results
        self.assertContains(response, 'Software Developer')

    def test_dates_for_job_in_job_admin_screen(self):
        self.client.login(username='admin', password='adminpass')

        # Get the change page for the Job model
        change_page_url = '/admin/crewcal/job/'

        # Issue a GET request to the change page
        response = self.client.get(change_page_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the job's name is displayed in the list view
        self.assertContains(response, 'Dates for Job')
        self.assertContains(response, 'Date_Entry')



class TestDateEntryAdmin(TestCase):
    def setUp(self):
        # Create a superuser for logging into the admin site
        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')

        # Create a sample Job for testing
        self.job = Job.objects.create(name='Software Developer', number='JD123', location='Cityville')

        # Create a sample DateEntry for testing
        self.date_entry = DateEntry.objects.create(
            job=self.job,
            date='2022-01-15',
            crew='Dev Team',
            notes='Project meeting',
            quantity='10'
        )

    def test_date_entry_displayed_in_admin_list(self):
        # Log in the admin user
        self.client.login(username='admin', password='adminpass')

        # Get the change page for the DateEntry model
        change_page_url = f'/admin/crewcal/dateentry/'

        # Issue a GET request to the change page
        response = self.client.get(change_page_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the date entry's date is displayed in the list view
        self.assertContains(response, 'Jan. 15, 2022')

    def test_date_entry_search_in_admin(self):
        # Log in the admin user
        self.client.login(username='admin', password='adminpass')

        # Get the search page for the DateEntry model
        search_url = f'/admin/crewcal/dateentry/?q=Dev'

        # Issue a GET request to the search page
        response = self.client.get(search_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the date entry's crew is found in the search results
        self.assertContains(response, 'Dev Team')