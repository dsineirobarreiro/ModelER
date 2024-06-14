from django.urls import path, include
from django.contrib.auth import views as auth_views

from . import views

app_name = "users"
urlpatterns = [
    path('accounts/signup/', views.SignupView.as_view(), name='signup'),
    path('accounts/login/', views.CustomLoginView.as_view(), name='login'),
    path("accounts/logout", auth_views.LogoutView.as_view(), name='logout'),
    path("accounts/password_change/", views.CustomPasswordChangeView.as_view(), name='password_change'),
    path("accounts/password_change/done/", views.CustomPasswordChangeDoneView.as_view(), name='password_change_done'),
    path("accounts/password_reset/", auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("accounts/password_reset/done/", auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("accounts/reset/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("accounts/reset/done/", auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]