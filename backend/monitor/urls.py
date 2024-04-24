from django.urls import path

from . import views

urlpatterns = [
    path("historical-data/", views.get_historical_data, name="historicalData"),
    path("abnormal-data/", views.get_abnormal_data, name="abnormalData"),
]