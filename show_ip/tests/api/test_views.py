from django.urls import reverse

from show_ip.tests.base_test_case import BaseCSVTestCase


class TestApiShowIpView(BaseCSVTestCase):
    url = reverse("showip:ip")
