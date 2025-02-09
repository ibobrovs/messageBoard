from django.contrib import admin
from django.urls import path, include
from MessageApp.views import home

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", home, name="home"),
    path("messageapp/", include("MessageApp.urls")),
]
