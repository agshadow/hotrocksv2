from django.urls import path

from crewcal import views

urlpatterns = [
    path("", views.home, name="home"),  
]