import json

from django.urls import reverse

from show_ip.tests.base_test_case import BaseShowTestCase


class TestApiShowIpView(BaseShowTestCase):
    url = reverse("show:ip-api")
    content_type = "Content-Type: application/json; charset=UTF-8"

    def test_get_ips_with_addresses_field_should_be_return_json_with_data(self, client, mock_get_ips):
        jso = json.dumps({"addresses": "example.pl"})
        rq = client.post(self.url, data=jso, content_type=self.content_type)

        assert b"localhost" in rq.content
        assert rq.status_code == 200

    def test_get_ips_with_empty_variables_should_be_return_ok_with_errors(self, client, mock_get_ips):
        jso = json.dumps({"addresses": ""})
        rq = client.post(self.url, data=jso, content_type=self.content_type)

        assert rq.status_code == 400

    def test_get_isp_with_incorect_type_should_be_return_status_400_end_get_error_message(self, client, mock_get_ips):
        rq = client.post(self.url, content_type=self.content_type, data={"address": "example.com"})

        assert rq.status_code == 400
        assert b"Type not supported" in rq.content
