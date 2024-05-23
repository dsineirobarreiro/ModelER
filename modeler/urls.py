from django.urls import path

from . import views

app_name = "modeler"
urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("model/", views.ModelListView.as_view(), name="model-list"),
    path("model/new/<str:llm>", views.ChatCreateView.as_view(), name="chat-create"),
    path("model/<str:llm>", views.ModelView.as_view(), name="model"),
    path("stream-http/", views.StreamView.as_view(), name="stream-http"),
    path("stream/", views.stream_http, name="stream"),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<str:section>', views.ProfileView.as_view(), name='profile'),
]
