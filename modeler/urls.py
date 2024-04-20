from django.urls import path, include
from . import views

app_name = "modeler"
urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("model/", views.ModelView.as_view(), name="model"),
]
