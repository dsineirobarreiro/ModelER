from django.urls import path, include
from . import views

app_name = "modeler"
urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("model/", views.ModelView.as_view(), name="model"),
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/login/', views.LoginView.as_view(), name='login'),
    path("accounts/", include("django.contrib.auth.urls"))
]
