from django.shortcuts import redirect
from django.contrib import admin
from django.urls import path
from django.http import HttpResponse


urlpatterns = [
    path("healthz/", lambda r: HttpResponse("ok")),
    path("", lambda r: redirect("/admin/")),
    path("admin/", admin.site.urls),
]
