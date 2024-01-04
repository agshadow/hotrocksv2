import django_tables2 as tables
from report.models import IncidentReport

class IncidentReportTable(tables.Table):
    class Meta:
        model = IncidentReport