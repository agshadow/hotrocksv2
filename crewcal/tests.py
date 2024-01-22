from django.test import TestCase, RequestFactory
from django.urls import reverse
from datetime import date
from .models import Job, DateEntry, UserProfile, Workgroup, CompanyWorkgroup, Company
from django.contrib.auth.models import User
from crewcal.utils import transpose_dates, get_calendar_for_date_range
from crewcal.forms import DateEntryForm

class TestCalHome(TestCase):       
    def setUp(self):
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.job = Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton",
            company_workgroup = self.cw,
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
        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.client.login(username='admin', password='adminpass')        
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw,
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
    
    def test_should_display_calendar_items_for_user(self):

        self.user = User.objects.create_user(username='accentureuser', password='adminpass', email='admin@example.com')
        self.wg1 = Workgroup.objects.create(name="Sydney")
        self.cp1 = Company.objects.create(name="Accenture")
        self.cw1 = CompanyWorkgroup.objects.create(company=self.cp1, workgroup=self.wg1)
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw1
        )

        self.job2 = Job.objects.create(
            name = "Marigold Stage 1",
            number = "22-02-5233",
            location = "Tarneit Road, Tarneit",
            company_workgroup = self.cw1
        )
        self.entry2_1 = DateEntry.objects.create(
            job = self.job2,
            date = date(2024,1,9),
            crew = "Roger",
            notes = "Prime and Sami",
            quantity = "205T 20SI",

        )
        url = "/cal/?datefrom=20240108&dateto=20240114"
        response = self.client.get(url)
        self.assertNotContains(response, "Roger")

    def test_should_be_able_to_go_to_next_date_range(self):
        
        url = "/cal/?datefrom=20240108&dateto=20240114"
        response = self.client.get(url)
        self.assertContains(response, "Next")
        self.assertContains(response, "/cal/?datefrom=20240108&dateto=20240114&goto=next_week")

    def test_should_be_able_to_go_to_previous_date_range(self):
        
        url = "/cal/?datefrom=20240108&dateto=20240114"
        response = self.client.get(url)
        self.assertContains(response, "Prev")
        self.assertContains(response, "/cal/?datefrom=20240108&dateto=20240114&goto=prev_week")

class TestHomePageAuthentication(TestCase):
    def test_should_take_you_to_login_screen_if_not_logged_in(self):
        url = "/cal/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
        self.assertIn('/accounts/login',response.url)

    def test_should_render_calendar_screen_if_logged_in(self):
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw
        )
        self.client.login(username='admin', password='adminpass')
        
        url = "/cal/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn('/cal/',response.request['PATH_INFO'])
        self.assertContains(response, "Calendar")

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
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton",
            company_workgroup = self.cw,
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
            location = "Grange Road, Plumpton",
            company_workgroup = self.cw,
        )
        self.assertIn("Hibiscus",str(job))
        self.assertIn("22-02-4423",str(job))
        self.assertIn("Grange Road, Plumpton",str(job))


class TestDateEntryModel(TestCase):
    def setUp(self):
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.job = Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton",
            company_workgroup = self.cw,
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
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw,
        )
        # Create a sample job for testing
        self.job = Job.objects.create(
            name='Software Developer', 
            number='JD123', 
            location='Cityville',
            company_workgroup = self.cw,
            )


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
        search_url = '/admin/crewcal/job/?q=Software'

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
        self.assertContains(response, 'Associated Dates')
        self.assertContains(response, 'Date Entries')


class TestDateEntryAdmin(TestCase):
    def setUp(self):
        # Create a superuser for logging into the admin site
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw,
        )
        # Create a sample Job for testing
        self.job = Job.objects.create(
            name='Software Developer', 
            number='JD123', 
            location='Cityville',
            company_workgroup = self.cw,
        )
            

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
        change_page_url =      '/admin/crewcal/dateentry/'

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
        search_url = '/admin/crewcal/dateentry/?q=Dev'

        # Issue a GET request to the search page
        response = self.client.get(search_url)

        # Check if the response status is 200 (OK)
        self.assertEqual(response.status_code, 200)

        # Check if the date entry's crew is found in the search results
        self.assertContains(response, 'Dev Team')


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

        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw,
        )
        users = UserProfile.objects.count()
        self.assertEqual(users, 1)
        user = UserProfile.objects.first()
        self.assertEqual(user.company_workgroup,self.cw)

    def test_should_display_user_profile_in_admin_user_change_screen(self):
        #tests the Stacked Inline and UserAdmin Classes
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw,
        )
        self.client.login(username='admin', password='adminpass')

        change_page_url = '/admin/auth/user/1/change/'
        response = self.client.get(change_page_url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User Profile')
        self.assertContains(response, 'Company')

class TestRestrictedPage(TestCase):
    def setUp(self):
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw,
        )
    def test_restricted_page_renders(self):
        url =    "/cal/restricted_page"
        self.client.login(username='admin', password='adminpass')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You are logged in")

class TestAccountFunctionality(TestCase):
    def test_should_be_able_to_login_using_accounts_login(self):
        url = "/accounts/login/"
        response = self.client.get(url)
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.user = User.objects.create_superuser(username='admin', password='adminpass', email='admin@example.com')
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")
        self.assertContains(response, "Username")
        self.assertContains(response, "Password")

       
        data = {
            'username' : 'admin',
            'password' : 'adminpass',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

class TestTransposeDates(TestCase):
    def test_should_return_dates_formatted_correctly(self):
        transposed_format_required = {
            '0':"", 
            '1': "Mon, Jan 8",
            '2': "Tue, Jan 9",
            '3': "Wed, Jan 10",
            '4': "Thu, Jan 11",
            '5': "Fri, Jan 12",
            '6': "Sat, Jan 13",
            '7': "Sun, Jan 14",
        }
        datefrom = date(2024, 1, 8)
        transposed = transpose_dates(datefrom)
        self.assertEqual(transposed, transposed_format_required)
        self.assertTrue("0" in transposed)
        
    def test_should_return_todays_date_if_not_specified(self):
        transposed = transpose_dates()
        self.assertTrue("0" in transposed)
        self.assertEqual(date.today().strftime("%a, %b %d"), transposed["1"])

class TestGetCalendarForWeek(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)
        self.user = User.objects.create_user(username='unisysuser', 
                                        password='adminpass', 
                                        email='admin@example.com',)
        self.userprofile = UserProfile.objects.create(
            user = self.user,
            company_workgroup = self.cw,)
        self.wg1 = Workgroup.objects.create(name="Sydney")
        self.cp1 = Company.objects.create(name="Accenture")
        self.cw1 = CompanyWorkgroup.objects.create(company=self.cp1, workgroup=self.wg1)

        self.user1 = User.objects.create_user(username='accentureuser', 
                                             password='adminpass', 
                                             email='admin@example.com')

        userprofile1 = UserProfile.objects.create(
            user = self.user1,
            company_workgroup = self.cw1,
                )

        self.job = Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton",
            company_workgroup = self.cw
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
        self.job1 = Job.objects.create(
                    name = "Bridgefield Stage 1",
                    number = "22-02-3152",
                    location = "Greigs Rd Rockbank",
                    company_workgroup = self.cw1,
                )
        self.entry1_1 = DateEntry.objects.create(
                    job = self.job1,
                    date = date(2024, 1, 8),
                    crew = "Lee",
                    notes = "Prime and Sami",
                    quantity = "100T 10N",
                )
        self.job2 = Job.objects.create(
                    name = "Highett Station",
                    number = "22-02-4555",
                    location = "Highett Road Highett Station",
                    company_workgroup = self.cw
                )
        self.entry2_1 = DateEntry.objects.create(
                    job = self.job2,
                    date = date(2024, 1, 9),
                    crew = "Plugga",
                    notes = "Prime and Sami",
                    quantity = "500T 20SI",
                )
        self.entry2_1 = DateEntry.objects.create(
                    job = self.job2,
                    date = date(2024, 1, 10),
                    crew = "Plugga",
                    notes = "Prime and Sami",
                    quantity = "500T 20SI",
                )
    def test_should_return_jobs_formatted_per_crew(self):

        
        self.client.login(username='unisysuser', password='adminpass')
        
        url = "/cal/?datefrom=20240108&dateto=20240114"
        datefrom = date(2024, 1, 8)
        dateto = date(2024, 1, 14)
        response = self.client.get(url)
        url = reverse('cal_home')  # Replace 'your_url_name' with the actual URL name of your view
        request = self.factory.get(url) 
        request.user = self.user

        formatted_data = get_calendar_for_date_range(request, datefrom, dateto)
        self.assertTrue("0" in formatted_data)
        self.assertTrue("1" in formatted_data["0"])
        self.assertTrue("7" in formatted_data["0"])
        self.assertIn("Jeff", formatted_data["0"]["0"])





class TestDateEntryForm(TestCase):
    def setUp(self):
        self.form = DateEntryForm

    def test_should_be_able_to_create_valid_date_entry_form(self):
        
        self.assertTrue(issubclass(self.form, DateEntryForm))
        #check fields are in the meta
        self.assertTrue('notes' in self.form.Meta.fields)
        self.assertTrue('quantity' in self.form.Meta.fields)
        self.assertTrue('date' in self.form.Meta.fields)
        self.assertTrue('crew' in self.form.Meta.fields)

class TestCalendarUpdatePage(TestCase):
    def setUp(self):
        self.wg = Workgroup.objects.create(name="Melbourne")
        self.cp = Company.objects.create(name="Unisys")
        self.cw = CompanyWorkgroup.objects.create(company=self.cp, workgroup=self.wg)

        self.job = Job.objects.create(
            name = "Hibiscus Stage 1",
            number = "22-02-4423",
            location = "Grange Road, Plumpton",
            company_workgroup = self.cw,
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
        self.form = DateEntryForm

    def test_should_render_update_page_with_correct_response(self):
        url = f"/cal/update/{self.entry1.id}/?datefrom=20240108&dateto=20240114"
        response = self.client.get(url)

        self.assertTemplateUsed(response, 'update.html')
        self.assertEqual(response.status_code,200)

    def test_should_return_404_if_date_range_missing(self):
        url = f"/cal/update/{self.entry1.id}/"
        response = self.client.get(url)

        self.assertEqual(response.status_code,404)
        