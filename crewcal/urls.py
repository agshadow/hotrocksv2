from django.urls import path

from crewcal import views

urlpatterns = [
    path("", views.cal_home, name="cal_home"),  
    path("restricted_page", views.restricted_page, name="restricted_page"),
    path("update/<int:job_id>/", views.cal_update, name="cal_update"),
]