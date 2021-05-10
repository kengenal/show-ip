from django.urls import path

from show_ip.views import ShowIpView

app_name = "show"

urlpatterns = [
    path("", ShowIpView.as_view(), name="ip")
]
