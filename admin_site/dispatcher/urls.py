from django.urls import path
from dispatcher.views import (
    RequestListView, RequestDetailView,
    DigestView, HousesView, SettingsView,
)

urlpatterns = [
    path("", RequestListView.as_view(), name="request_list"),
    path("request/<int:pk>/", RequestDetailView.as_view(), name="request_detail"),
    path("digest/", DigestView.as_view(), name="digest"),
    path("houses/", HousesView.as_view(), name="houses"),
    path("settings/", SettingsView.as_view(), name="settings"),
]
