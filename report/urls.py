from django.urls import path

from report import views

urlpatterns = [
    path("list_reports/", views.list_reports, name="list_reports"),
    path("view_report/<int:report_id>/", views.view_report, name="view_report"),
    path("add_report/", views.view_report, name="add_report"),
    path("new/", views.new_report, name="new_report"),
    path("pdf_report/<int:report_id>/", views.pdf_report, name="pdf_report"),
]