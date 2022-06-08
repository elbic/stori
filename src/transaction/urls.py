from django.urls import path

from .views import index, process_csv

urlpatterns = [
    path("", index, name="index"),
    path("process/", process_csv, name="process_csv"),
]
