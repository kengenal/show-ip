from django.urls import path

from show_ip.views import ShowIpView

urlpatterns = [
    path("", ShowIpView.as_view())
]
