from django.urls import path

from crewcal import views

urlpatterns = [
    path("", views.cal_home, name="cal_home"),
    path("restricted_page", views.restricted_page, name="restricted_page"),
    path("update/<int:job_id>/", views.cal_update, name="cal_update"),
    path("job/create/", views.create_job, name="create_job"),
    path("job/update/<int:job_id>/", views.update_job, name="update_job"),
    path("job/delete/<int:job_id>/", views.delete_job, name="delete_job"),
    path("jobs/view/", views.view_jobs, name="view_jobs"),
    path("shift/create/", views.create_shift, name="create_shift"),
    path("shift/read/", views.read_shift, name="read_shift"),
    path("shift/update/<int:report_id>/", views.update_shift, name="update_shift"),
    path("shift/delete/<int:report_id>/", views.delete_shift, name="delete_shift"),
    path("create_date_entry/", views.create_date_entry, name="create_date_entry"),
    path("job_search/", views.job_search, name="job_search"),
]
