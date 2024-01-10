from django.test import TestCase
from datetime import date
from .models import Job, DateEntry

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
        self.assertContains(response, "Jeff")

    def test_should_display_calendar_for_week(self):
        url = "/cal/?datefrom=20240108&dateto=20240114"
        response = self.client.get(url)
        self.assertContains(response, "Mon, Jan 8")
        self.assertNotContains(response, "Mon, Jan 15")
        self.assertContains(response, "Sun, Jan 14")

    def test_should_be_able_render_cal_page_with_jobs_for_those_dates(self):
        url = "/cal/"
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