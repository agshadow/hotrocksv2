from django.test import TestCase, override_settings
import uuid
import tempfile
from base64 import b64decode
from datetime import datetime, timezone
from datetime import date
from report.models import IncidentReport, IncidentTypeChoice, IncidentReportFiles
from report.forms import (
    NewIncidentReportForm,
    UpdateIncidentReportForm,
    IncidentReportFileForm,
)
from django.core.files.uploadedfile import SimpleUploadedFile


class TestIncidentReportModel(TestCase):
    def test_should_be_able_to_create_a_incident_report_model(self):
        reports = IncidentReport.objects.count()
        self.assertEqual(reports, 0)

    def test_should_add_incident_report_model(self):
        self.incident_report = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site="Footscray",
            reported_by="user",
            description="operator was injured",
            sign_off="user",
            sign_off_date=date(2023, 1, 2),
        )
        report1 = IncidentReport.objects.first()
        self.assertEqual(
            datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc), report1.incident_date
        )
        reports = IncidentReport.objects.count()
        self.assertEqual(reports, 1)


class TestIncidentReportFilesModel(TestCase):
    def setUp(self):
        self.incident_report = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site="Footscray",
            reported_by="user",
            description="operator was injured",
            sign_off="user",
            sign_off_date=date(2023, 1, 2),
        )
        # Base64 encoded version of a single pixel GIF image
        image = "R0lGODdhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs="
        self.image = b64decode(image)

    def test_should_be_able_to_create_a_incident_report_file_model(self):
        files = IncidentReportFiles.objects.count()
        self.assertEqual(files, 0)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_should_add_incident_report_file_model(self):
        new_random_file_name = str(uuid.uuid4())
        file = SimpleUploadedFile(new_random_file_name, self.image)

        self.incident_report_file = IncidentReportFiles.objects.create(
            incident_report=self.incident_report,
            filename="test.gif",
            file=file,
        )

        incident_report_file1 = IncidentReportFiles.objects.first()
        self.assertEqual("test.gif", incident_report_file1.filename)
        self.assertEqual(new_random_file_name, incident_report_file1.file.name)
        self.assertEqual(self.incident_report, incident_report_file1.incident_report)
        incident_report_files_count = IncidentReportFiles.objects.count()
        self.assertEqual(incident_report_files_count, 1)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_should_add_incident_report_file_model_and_auto_geneate_random_file_name(
        self,
    ):
        new_random_file_name = str(uuid.uuid4())
        file = SimpleUploadedFile(new_random_file_name, self.image)

        self.incident_report_file = IncidentReportFiles.objects.create(
            incident_report=self.incident_report,
            filename="test.gif",
            file=file,
        )

        incident_report_file1 = IncidentReportFiles.objects.first()
        self.assertEqual("test.gif", incident_report_file1.filename)
        self.assertEqual(new_random_file_name, incident_report_file1.file.name)
        self.assertEqual(self.incident_report, incident_report_file1.incident_report)
        incident_report_files_count = IncidentReportFiles.objects.count()
        self.assertEqual(incident_report_files_count, 1)


class TestListReports(TestCase):
    def setUp(self):
        self.incident_report = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site="Footscray",
            reported_by="user",
            description="operator was injured",
            sign_off="user",
            sign_off_date=date(2023, 1, 2),
        )

    def test_list_reports(self):
        url = "/report/list_reports/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertIn(self.incident_report.site, str(response.content))
        self.assertIn(self.incident_report.sign_off, str(response.content))

    def test_edit_button_should_link_to_edit_page(self):
        url = "/report/list_reports/"
        response = self.client.get(url)
        self.assertContains(response, 'action="/report/update/')

    def test_should_render_delete_button_on_list_reports_page_and_target_delete_con(
        self,
    ):
        url = "/report/list_reports/"
        response = self.client.get(url)
        self.assertContains(response, 'action="/report/delete_confirmation/')

    def test_should_display_link_for_new_report(self):
        url = "/report/list_reports/"
        response = self.client.get(url)
        self.assertContains(response, '<a href="/report/new/">New Incident Report</a>')


class TestIncidentReportFileForm(TestCase):
    def setUp(self):
        self.form = IncidentReportFileForm
        # Base64 encoded version of a single pixel GIF image
        image = "R0lGODdhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs="
        self.image = b64decode(image)

    def test_should_be_able_to_create_valid_incident_report_file_form(self):
        self.assertTrue(issubclass(self.form, IncidentReportFileForm))
        # check fields are in the meta
        self.assertTrue("file" in self.form.Meta.fields)
        self.assertTrue("filename" in self.form.Meta.fields)
        self.assertTrue("incident_report" in self.form.Meta.fields)


class TestNewReport(TestCase):
    def setUp(self):
        """self.incident_report  = IncidentReport.objects.create(
            incident_type = IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site = "Footscray",
            reported_by = "user",
            description = "operator was injured",
            sign_off = "user",
            sign_off_date=date(2023, 1, 2),
        )"""
        self.form = NewIncidentReportForm
        image = "R0lGODdhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs="
        self.image = b64decode(image)

    def test_should_render_new_page_with_correct_response(self):
        url = "/report/new/"
        response = self.client.get(url)
        self.assertTemplateUsed(response, "new.html")
        self.assertEqual(response.status_code, 200)

    def test_should_have_valid_form_in_new_page(self):
        self.assertTrue(issubclass(self.form, NewIncidentReportForm))
        # check fields are in the meta
        self.assertTrue("incident_type" in self.form.Meta.fields)
        self.assertTrue("incident_date" in self.form.Meta.fields)
        self.assertTrue("site" in self.form.Meta.fields)
        self.assertTrue("sign_off" in self.form.Meta.fields)

        form = self.form(
            {
                "incident_type": IncidentTypeChoice.INJURY,
                "incident_date": datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
                "site": "Footscray",
                "reported_by": "user1",
                "description": "operator was injured",
                "sign_off": "user",
                "sign_off_date": date(2023, 1, 2),
            }
        )

        self.assertTrue(form.is_valid())

    def test_should_be_invalid_when_site_is_empty(self):
        form = self.form(
            {
                "incident_type": IncidentTypeChoice.INJURY,
                "incident_date": datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
                "site": "",
                "reported_by": "user1",
                "description": "operator was injured",
                "sign_off": "user",
                "sign_off_date": date(2023, 1, 2),
            }
        )

        self.assertFalse(form.is_valid())

    def test_should_display_form_in_new_page(self):
        url = "/report/new/"
        response = self.client.get(url)

        self.assertContains(response, "<form")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, "<label for")

    def test_should_display_incident_report_file_form_in_new_page(self):
        url = "/report/new/"
        response = self.client.get(url)

        self.assertContains(response, "<form")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, '<label for="id_file">File:</label>')

    def test_should_save_new_report_when_data_is_valid_in_new_form(self):
        data = {
            "incident_type": IncidentTypeChoice.INJURY,
            "incident_date": datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            "site": "Footscray",
            "reported_by": "user1",
            "description": "operator was injured",
            "sign_off": "user",
            "sign_off_date": date(2023, 1, 2),
        }

        url = "/report/new/"
        response = self.client.post(url, data)

        self.assertRedirects(response, expected_url="/report/list_reports/")
        self.assertEqual(IncidentReport.objects.count(), 1)

    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_should_save_file_in_new_form(self):
        file = SimpleUploadedFile("test.gif", self.image)
        data = {
            "incident_report": "none",
            "filename": "nonefilename",
            "incident_type": IncidentTypeChoice.INJURY,
            "incident_date": datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            "site": "Footscray",
            "reported_by": "user1",
            "description": "operator was injured",
            "sign_off": "user",
            "sign_off_date": date(2023, 1, 2),
            "file": file,
        }

        url = "/report/new/"
        response = self.client.post(url, data)

        self.assertRedirects(response, expected_url="/report/list_reports/")
        self.assertEqual(IncidentReport.objects.count(), 1)
        self.assertEqual(IncidentReportFiles.objects.count(), 1)


class TestNewReportFile(TestCase):
    def setUp(self):
        self.incident_report = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site="Footscray",
            reported_by="user",
            description="operator was injured",
            sign_off="user",
            sign_off_date=date(2023, 1, 2),
        )
        self.form = NewIncidentReportForm
        image = "R0lGODdhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs="
        self.image = b64decode(image)

    """@override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def test_should_save_file_in_new_form(self):
        
        file = SimpleUploadedFile("test.gif", self.image)
        data = {
            'incident_report' : self.incident_report,
            'filename' : "nonefilename",
            'file': file,

        }
        

        url = f"/report/new/"
        response = self.client.post(url, data)

        self.assertRedirects(response, expected_url='/report/list_reports/')
        self.assertEqual(IncidentReport.objects.count(), 1)
        self.assertEqual(IncidentReportFiles.objects.count(), 1)"""


class TestPdfResport(TestCase):
    def setUp(self):
        self.incident_report = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site="Footscray",
            reported_by="user",
            description="operator was injured",
            sign_off="user",
            sign_off_date=date(2023, 1, 2),
        )

    def test_should_display_pdf_of_incident_report(self):
        url = f"/report/pdf_report/{self.incident_report.id}/"
        response = self.client.get(url)
        self.assertEqual(200, response.status_code)
        self.assertEqual(
            response.get("Content-Disposition"), 'attachment; filename="report.pdf"'
        )


class TestDetailPage(TestCase):
    @override_settings(MEDIA_ROOT=tempfile.gettempdir())
    def setUp(self):
        self.incident_report = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site="Footscray",
            reported_by="user",
            description="operator was injured",
            sign_off="user",
            sign_off_date=date(2023, 1, 2),
        )
        self.incident_report2 = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 3, 7, 0, tzinfo=timezone.utc),
            site="Beechworth",
            reported_by="user2",
            description="slipped on rock",
            sign_off="user2",
            sign_off_date=date(2023, 1, 2),
        )

        # Base64 encoded version of a single pixel GIF image
        image = "R0lGODdhAQABAIABAP///wAAACwAAAAAAQABAAACAkQBADs="
        self.image = b64decode(image)
        new_random_file_name = str(uuid.uuid4())
        file = SimpleUploadedFile(new_random_file_name, self.image)

        self.incident_report_file = IncidentReportFiles.objects.create(
            incident_report=self.incident_report,
            filename="test.gif",
            file=file,
        )

    def test_should_display_detail_page(self):
        url = f"/report/detail/{self.incident_report.id}/"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "detail.html")

    def test_should_display_report_details_on_detail_page(self):
        url = f"/report/detail/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertContains(response, self.incident_report.incident_type)
        # dates dont display same
        # self.assertContains(response, self.incident_report.incident_date)
        self.assertContains(response, self.incident_report.site)
        self.assertContains(response, self.incident_report.reported_by)
        self.assertContains(response, self.incident_report.description)
        self.assertContains(response, self.incident_report.sign_off)
        # dates dont display same
        # self.assertContains(response, self.incident_report.sign_off_date)
        self.assertNotContains(response, self.incident_report2.site)

    def test_should_display_file_download_link(self):
        url = f"/report/detail/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertContains(response, "test.gif")


class TestUpdatePage(TestCase):
    def setUp(self):
        self.incident_report = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site="Footscray",
            reported_by="user",
            description="operator was injured",
            sign_off="user",
            sign_off_date=date(2023, 1, 2),
        )
        self.form = UpdateIncidentReportForm

    def test_should_render_update_page_with_correct_response(self):
        url = f"/report/update/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertTemplateUsed(response, "update.html")
        self.assertEqual(response.status_code, 200)

    def test_should_have_valid_form_in_update_page(self):
        self.assertTrue(issubclass(self.form, UpdateIncidentReportForm))
        # check fields are in the meta
        self.assertTrue("incident_type" in self.form.Meta.fields)
        self.assertTrue("incident_date" in self.form.Meta.fields)
        self.assertTrue("site" in self.form.Meta.fields)
        self.assertTrue("sign_off" in self.form.Meta.fields)

        # test valid form
        # updates self.task with new data

        form = self.form(
            {
                "incident_type": IncidentTypeChoice.INJURY,
                "incident_date": datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
                "site": "Footscray",
                "reported_by": "user1",
                "description": "operator was injured",
                "sign_off": "user",
                "sign_off_date": date(2023, 1, 2),
            },
            instance=self.incident_report,
        )

        self.assertTrue(form.is_valid())

        form.save()

        self.assertEqual(self.incident_report.reported_by, "user1")

    def test_should_be_invalid_when_title_is_empty(self):
        form = self.form(
            {
                "incident_type": IncidentTypeChoice.INJURY,
                "incident_date": datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
                "site": "",
                "reported_by": "user1",
                "description": "operator was injured",
                "sign_off": "user",
                "sign_off_date": date(2023, 1, 2),
            }
        )

        self.assertFalse(form.is_valid())

    def test_should_render_form_in_update_page(self):
        url = f"/report/update/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertContains(response, "<form")
        self.assertContains(response, "csrfmiddlewaretoken")
        self.assertContains(response, "<label for")
        self.assertContains(response, "Footscray")

    def test_should_render_error_when_site_is_blank_in_update_page(self):
        data = {
            "incident_type": IncidentTypeChoice.INJURY,
            "incident_date": datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            "site": "",
            "reported_by": "user1",
            "description": "operator was injured",
            "sign_off": "user",
            "sign_off_date": date(2023, 1, 2),
        }

        url = f"/report/update/{self.incident_report.id}/"
        response = self.client.post(url, data)
        self.assertContains(response, '<ul class="errorlist"')
        self.assertContains(response, "This field is required.")

    def test_should_update_task_when_data_is_valid(self):
        data = {
            "incident_type": IncidentTypeChoice.INJURY,
            "incident_date": datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            "site": "Broadmeadows",
            "reported_by": "user1",
            "description": "operator was injured",
            "sign_off": "user",
            "sign_off_date": date(2023, 1, 2),
        }

        url = f"/report/update/{self.incident_report.id}/"
        response = self.client.post(url, data)

        # cant use these because it redirects
        # self.assertNotContains(response, '<ul class="errorlist"')
        # self.assertNotContains(response, 'This field is required.')
        self.assertRedirects(response, expected_url="/report/list_reports/")
        self.assertEqual(IncidentReport.objects.count(), 1)
        self.assertEqual(IncidentReport.objects.first().site, "Broadmeadows")


class TestDeletePage(TestCase):
    def setUp(self):
        self.incident_report = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site="Footscray",
            reported_by="user",
            description="operator was injured",
            sign_off="user",
            sign_off_date=date(2023, 1, 2),
        )

    def test_should_delete_task_on_delete_page(self):
        self.assertEqual(IncidentReport.objects.count(), 1)

        url = f"/report/delete/{self.incident_report.id}/"
        response = self.client.post(url)

        self.assertRedirects(response, expected_url="/report/list_reports/")
        self.assertEqual(IncidentReport.objects.count(), 0)

    def test_should_404_when_invalid_item_is_sent_to_delete_page(self):
        self.assertEqual(IncidentReport.objects.count(), 1)

        url = "/report/delete/2/"
        response = self.client.post(url)

        self.assertEqual(response.status_code, 404)


class TestDeleteConfirmationPage(TestCase):
    def setUp(self):
        self.incident_report = IncidentReport.objects.create(
            incident_type=IncidentTypeChoice.INJURY,
            incident_date=datetime(2023, 1, 1, 7, 0, tzinfo=timezone.utc),
            site="Footscray",
            reported_by="user",
            description="operator was injured",
            sign_off="user",
            sign_off_date=date(2023, 1, 2),
        )

    def test_should_display_delete_confirmation_page(self):
        url = f"/report/delete_confirmation/{self.incident_report.id}/"
        response = self.client.get(url)
        self.assertTemplateUsed(response, "delete_confirmation.html")
        self.assertEqual(response.status_code, 200)

    def test_should_display_item_to_delete_on_delete_confirmation_page(self):
        url = f"/report/delete_confirmation/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertContains(response, self.incident_report.site)
        self.assertContains(response, self.incident_report.reported_by)
        self.assertContains(response, self.incident_report.description)
        self.assertIn(self.incident_report.incident_type.label, str(response.content))

    def test_should_render_form_button_delete(self):
        url = f"/report/delete_confirmation/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertContains(
            response,
            f'<form method="get" action="/report/delete/{self.incident_report.id}/">',
        )

    def test_should_render_form_button_cancel(self):
        url = f"/report/delete_confirmation/{self.incident_report.id}/"
        response = self.client.get(url)

        self.assertContains(
            response, '<form method="get" action="/report/list_reports/">'
        )
