from django.urls import path, register_converter

from . import views, converters

register_converter(converters.LlmConverter, "model")
register_converter(converters.DiagramConverter, "diagram")
register_converter(converters.TokenConverter, "token")

app_name = "modeler"
urlpatterns = [
    path("", views.IndexView.as_view(), name='index'),
    path("model/", views.ModelListView.as_view(), name="model-list"),
    path("model/<model:llm>", views.DiagramSelectionView.as_view(), name="diagram_selection"),
    path("model/<model:llm>/<diagram:pk>", views.ModelView.as_view(), name="model"),
    path("stream-http/", views.StreamView.as_view(), name="stream-http"),
    path("stream/", views.stream_http, name="stream"),
    path('profile/', views.ProfileGeneralView.as_view(), name='profile'),
    path('profile/general', views.ProfileGeneralView.as_view(), name='profile_general'),
    path('profile/settings', views.ProfileSettingsView.as_view(), name='profile_settings'),
    path('profile/diagrams', views.ProfileDiagramsView.as_view(), name='profile_diagrams'),
    path('profile/tokens', views.ProfileTokensView.as_view(), name='profile_tokens'),
    path('token/<token:pk>/edit', views.TokenView.as_view(), name='token'),
    path('diagram/<diagram:pk>/edit', views.DiagramView.as_view(), name='diagram'),
    path('diagram/<diagram:pk>/<str:format>', views.DiagramDownloadView.as_view(), name='diagram-download')
]
