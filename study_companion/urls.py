from django.urls import path
from . import views
urlpatterns = [
    path('', views.study_companion, name="study_companion")
]