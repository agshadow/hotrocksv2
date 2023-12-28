from django.urls import path

from report import views

urlpatterns = [
    path("list_reports/", views.list_reports, name="list_reports"),
    path("view_report/<int:report_id>/", views.view_report, name="view_report"),
]