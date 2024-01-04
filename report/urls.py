from django.urls import path

from report import views
from report.tables import IncidentReportTable

urlpatterns = [
    path("list_reports/", views.list_reports, name="list_reports"),
    path("add_report/", views.view_report, name="add_report"),
    path("new/", views.new_report, name="new_report"),
    path("detail/<int:report_id>/", views.detail, name="detail"),
    path("pdf_report/<int:report_id>/", views.pdf_report, name="pdf_report"),
    path("update/<int:report_id>/", views.update, name="update"),
    path("delete/<int:report_id>/", views.delete, name="delete"),
    path("delete_confirmation/<int:report_id>/", views.delete_confirmation, name="delete_confirmation"),
]