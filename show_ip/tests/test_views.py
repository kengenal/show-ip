from django.urls import reverse

from show_ip.tests.base_test_case import BaseShowTestCase


class TestShowIpView(BaseShowTestCase):
    url = reverse("show:ip")

    def test_get_ips_with_addresses_field_should_be_return_template_with_data(self, client, mock_get_ips):
        rq = client.post(self.url, data={"addresses": "example.pl"})

        assert b"localhost" in rq.content
        assert rq.status_code == 200

    def test_get_ips_with_empty_variables_should_be_return_ok_with_errors(self, client, mock_get_ips):
        rq = client.post(self.url, data={"addresses": ""})

        assert rq.status_code == 200
