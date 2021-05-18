from django.urls import reverse

import show_ip
from show_ip.tests.base_test_case import BaseCSVTestCase
from show_ip.views import ShowIpView
from django.core.files.uploadedfile import SimpleUploadedFile


def mock(*args, **kwargs):
    return [{"ip": "localhost", "port": 443, "ssl": None}]


class TestShowIpView(BaseCSVTestCase):
    def test_get_ips_with_addresses_field_should_be_return_template_with_data(self, client, monkeypatch):
        monkeypatch.setattr(show_ip.views, "get_ips", mock)
        rq = client.post(reverse("show:ip"), data={"addresses": "example.pl"})

        assert b"localhost" in rq.content
        assert rq.status_code == 200

    def test_get_ips_with_empty_variables_should_be_return_ok_with_errors(self, client, monkeypatch):
        monkeypatch.setattr(show_ip.views, "get_ips", mock)
        rq = client.post(reverse("show:ip"), data={"addresses": ""})

        assert rq.status_code == 200

    def test_get_ips_with_file_field_should_be_return_template_with_data(self, client, monkeypatch, load_csv):
        monkeypatch.setattr(show_ip.views, "get_ips", mock)
        with open(load_csv, 'rb') as file:
            rq = client.post(reverse("show:ip"), data={"file": SimpleUploadedFile(file.name, file.read())})

            assert b"localhost" in rq.content
            assert rq.status_code == 200

    def test_get_empty_file_should_be_return_status_ok_with_form_errors(self, client, monkeypatch, load_empty_csv):
        monkeypatch.setattr(show_ip.views, "get_ips", mock)
        with open(load_empty_csv, 'rb') as file:
            rq = client.post(reverse("show:ip"), data={"file": SimpleUploadedFile(file.name, file.read())})

            assert rq.status_code == 200

    def test_with_option_download_file_should_be_return_file_and_set_headers(self, client, monkeypatch):
        monkeypatch.setattr(show_ip.views, "get_ips", mock)
        rq = client.post(reverse("show:ip"), data={"addresses": "example.pl", "get_scv": True})

        assert rq.headers["Content-Disposition"] == 'attachment; filename="host.csv"'
        assert rq.headers["Content-Type"] == "text/csv"
        assert b'host,ip,port,ssl,errors\r\n,localhost,443,,-\r\n' in rq.content
        assert rq.status_code == 200
