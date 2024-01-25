from django.test import TestCase
from crewcal.forms import DateEntryForm, JobForm, DateEntryForm1


class TestDateEntryForm(TestCase):
    def setUp(self):
        self.form = DateEntryForm

    def test_should_be_able_to_create_valid_date_entry_form(self):
        self.assertTrue(issubclass(self.form, DateEntryForm))
        # check fields are in the meta
        self.assertTrue("notes" in self.form.Meta.fields)
        self.assertTrue("quantity" in self.form.Meta.fields)
        self.assertTrue("date" in self.form.Meta.fields)
        self.assertTrue("crew" in self.form.Meta.fields)


class TestDateEntryForm1(TestCase):
    def setUp(self):
        self.form = DateEntryForm1

    def test_should_be_able_to_create_valid_date_entry_form(self):
        self.assertTrue(issubclass(self.form, DateEntryForm1))
        # check fields are in the meta
        self.assertTrue("notes" in self.form.Meta.fields)
        self.assertTrue("quantity" in self.form.Meta.fields)
        self.assertTrue("date" in self.form.Meta.fields)
        self.assertTrue("crew" in self.form.Meta.fields)
        self.assertTrue("job" in self.form.Meta.fields)


class TestJobForm(TestCase):
    def setUp(self):
        self.form = JobForm

    def test_should_be_able_to_create_valid_date_entry_form(self):
        self.assertTrue(issubclass(self.form, JobForm))
        # check fields are in the meta
        self.assertTrue("name" in self.form.Meta.fields)
        self.assertTrue("number" in self.form.Meta.fields)
        self.assertTrue("location" in self.form.Meta.fields)
        self.assertTrue("company_workgroup" in self.form.Meta.fields)
