from django.test import TestCase

from datetime import datetime, timezone
from datetime import date
from report.models import IncidentReport, IncidentTypeChoice

class TestReports(TestCase):
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

    def test_incident_report_added(self):
        report1 = IncidentReport.objects.first()
        print(report1)
        self.assertEqual(
            datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc), 
            report1.incident_date
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
        self.assertEqual(response.context["report"].id, self.incident_report.id)
        self.assertIn(self.incident_report.site, str(response.content))
        
    def test_should_display_incident_type_from_IncidentTypeChoice(self):
        url = f"/report/view_report/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertEqual(200, response.status_code)
        self.assertEqual(response.context["report"].id, self.incident_report.id)
        self.assertIn(self.incident_report.incident_type.label, str(response.content))

    def test_should_display_pdf_of_incident_report(self):
        url = f"/report/pdf_report/{self.incident_report.id}/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEquals(response.get('Content-Disposition'),
                          'attachment; filename="report.pdf"'
        )
