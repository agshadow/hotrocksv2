from django.urls import path

from crewcal import views

urlpatterns = [
    path("", views.cal_home, name="cal_home"),
    path("restricted_page", views.restricted_page, name="restricted_page"),
    path("update/<int:job_id>/", views.cal_update, name="cal_update"),
    path("job/create/", views.create_job, name="create_job"),
    path("job/update/<int:report_id>/", views.update_job, name="update_job"),
    path("job/delete/<int:report_id>/", views.delete_job, name="delete_job"),
    path("jobs/view/", views.view_jobs, name="view_jobs"),
    path("date/create/", views.create_date, name="create_date"),
    path("create_date_entry/", views.create_date_entry, name="create_date_entry"),
    path("job_search/", views.job_search, name="job_search"),
]
