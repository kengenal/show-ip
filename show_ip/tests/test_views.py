from django.urls import reverse

from show_ip.tests.base_test_case import BaseShowApiTestCase


class TestShowIpView(BaseShowApiTestCase):
    url = reverse("show-api:ip")
