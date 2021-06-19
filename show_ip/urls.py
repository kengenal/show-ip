from django.urls import path

from show_ip.api.views import ShowIpAPIView
from show_ip.views import ShowIpView

app_name = "show"

urlpatterns = [
    path("", ShowIpView.as_view(), name="ip"),
    path("api/showip", ShowIpAPIView.as_view(), name="ip-api"),
]
