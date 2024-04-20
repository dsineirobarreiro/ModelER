from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"
urlpatterns = [
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path("accounts/logout", auth_views.LogoutView.as_view(), name='logout'),
]