from django.test import TestCase

from datetime import datetime, timezone
from datetime import date
from report.models import IncidentReport, IncidentTypeChoice
from report.forms import NewIncidentReportForm


class TestIncidentReportModel(TestCase):       

    def test_should_be_able_to_create_a_incident_report_model(self):
        reports = IncidentReport.objects.count()
        self.assertEqual(reports, 0)
        
    def test_should_add_incident_report_model(self):
        self.incident_report  = IncidentReport.objects.create(
            incident_type = IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site = "Footscray",
            reported_by = "user",
            description = "operator was injured",
            sign_off = "user",
            sign_off_date=date(2023, 1, 2),
        )
        report1 = IncidentReport.objects.first()
        self.assertEqual(
            datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc), 
            report1.incident_date
            )
        reports = IncidentReport.objects.count()
        self.assertEqual(reports, 1)


class TestListReports(TestCase):
    def setUp(self):
        self.incident_report  = IncidentReport.objects.create(
            incident_type = IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site = "Footscray",
            reported_by = "user",
            description = "operator was injured",
            sign_off = "user",
            sign_off_date=date(2023, 1, 2),
        )
    
    def test_list_reports(self):
        url = "/report/list_reports/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertIn(self.incident_report.site, str(response.content))
        self.assertIn(self.incident_report.sign_off, str(response.content))

    def test_edit_button_should_link_to_edit_page(self):
        pass


class TestNewReport(TestCase):
    def setUp(self):
        '''self.incident_report  = IncidentReport.objects.create(
            incident_type = IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site = "Footscray",
            reported_by = "user",
            description = "operator was injured",
            sign_off = "user",
            sign_off_date=date(2023, 1, 2),
        )'''
        self.form = NewIncidentReportForm
    
    def test_should_render_new_page_with_correct_response(self):
        url = f"/report/new/"
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'new.html')
        self.assertEqual(response.status_code,200)

    def test_should_have_valid_form_in_new_page(self):
        self.assertTrue(issubclass(self.form, NewIncidentReportForm))
        #check fields are in the meta
        self.assertTrue('incident_type' in self.form.Meta.fields)
        self.assertTrue('incident_date' in self.form.Meta.fields)
        self.assertTrue('site' in self.form.Meta.fields)
        self.assertTrue('sign_off' in self.form.Meta.fields)
        
        form = self.form({
            'incident_type': IncidentTypeChoice.INJURY,
            'incident_date': datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            'site' : "Footscray",
            'reported_by' : "user1",
            'description' : "operator was injured",
            'sign_off' : "user",
            'sign_off_date':date(2023, 1, 2),
        })

        self.assertTrue(form.is_valid())


    def test_should_be_invalid_when_title_is_empty(self):
        form = self.form({
            'incident_type': IncidentTypeChoice.INJURY,
            'incident_date': datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            'site' : "",
            'reported_by' : "user1",
            'description' : "operator was injured",
            'sign_off' : "user",
            'sign_off_date':date(2023, 1, 2),
        })

        self.assertFalse(form.is_valid())


    
    def test_should_display_form_in_new_page(self):
        url = f"/report/new/"
        response = self.client.get(url)

        self.assertContains(response, '<form')
        self.assertContains(response, 'csrfmiddlewaretoken')
        self.assertContains(response, '<label for')


    def test_should_save_new_report_when_data_is_valid_in_new_form(self):
        data = {
            'incident_type': IncidentTypeChoice.INJURY,
            'incident_date': datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            'site' : "Footscray",
            'reported_by' : "user1",
            'description' : "operator was injured",
            'sign_off' : "user",
            'sign_off_date':date(2023, 1, 2),
        }

        url = f"/report/new/"
        response = self.client.post(url, data)

        self.assertRedirects(response, expected_url='/report/list_reports/')
        self.assertEqual(IncidentReport.objects.count(), 1)

class TestViewReport(TestCase):
    def setUp(self):
        self.incident_report  = IncidentReport.objects.create(
            incident_type = IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site = "Footscray",
            reported_by = "user",
            description = "operator was injured",
            sign_off = "user",
            sign_off_date=date(2023, 1, 2),
        )
    def test_view_report(self):
        url = "/report/view_report/1/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertIn("View Report", str(response.content))

    def test_should_display_report_in_view_report(self):
        url = f"/report/view_report/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertIn(self.incident_report.site, str(response.content))
       
    def test_should_display_incident_type_from_IncidentTypeChoice(self):
        url = f"/report/view_report/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertIn(self.incident_report.incident_type.label, str(response.content))

#add test for delete report
        


class TestPdfResport(TestCase):
    def setUp(self):
        self.incident_report  = IncidentReport.objects.create(
            incident_type = IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site = "Footscray",
            reported_by = "user",
            description = "operator was injured",
            sign_off = "user",
            sign_off_date=date(2023, 1, 2),
        )
    def test_should_display_pdf_of_incident_report(self):
        url = f"/report/pdf_report/{self.incident_report.id}/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEquals(response.get('Content-Disposition'),
                          'attachment; filename="report.pdf"'
        )
