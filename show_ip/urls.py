from django.urls import path

from show_ip.views import index

urlpatterns = [
    path("", index)
]
