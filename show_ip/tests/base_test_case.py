from abc import ABC

from django.urls import reverse

from django.core.files.uploadedfile import SimpleUploadedFile
import pytest
import os
import csv

import show_ip


def mock(*args, **kwargs):
    return [{"ip": "localhost", "port": 443, "ssl": None}]


class BaseCSVTestCase:
    @pytest.fixture()
    def load_csv(self):
        path = os.path.abspath('test.csv')
        with open(path, mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(["www.example.com", "tak"])
            employee_writer.writerow(["www.example2.com"])
        yield path
        os.remove(path)

    @pytest.fixture()
    def load_empty_csv(self):
        path = os.path.abspath('test.csv')
        with open(path, mode='w') as employee_file:
            csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        yield path
        os.remove(path)

    @pytest.fixture()
    def load_random_file(self):
        path = os.path.abspath('test.txt')
        with open(path, mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(["www.example.com", "tak"])
        yield path
        os.remove(path)

    @pytest.fixture()
    def mock_get_ips(self, monkeypatch):
        monkeypatch.setattr(show_ip.views, "get_ips", mock)


class BaseShowTestCase(ABC, BaseCSVTestCase):
    url = None

    def test_get_ips_with_file_field_should_be_return_template_with_data(self, client, mock_get_ips, load_csv):
        with open(load_csv, 'rb') as file:
            rq = client.post(self.url, data={"file": SimpleUploadedFile(file.name, file.read())})

            assert b"localhost" in rq.content
            assert rq.status_code == 200

    def test_get_empty_file_should_be_return_status_ok_with_form_errors(self, client, mock_get_ips, load_empty_csv):
        with open(load_empty_csv, 'rb') as file:
            rq = client.post(self.url, data={"file": SimpleUploadedFile(file.name, file.read())})

            assert rq.status_code == 200

    def test_with_option_download_file_should_be_return_file_and_set_headers(self, client, mock_get_ips):
        rq = client.post(self.url, data={"addresses": "example.pl", "get_scv": True})

        assert rq.headers["Content-Disposition"] == 'attachment; filename="host.csv"'
        assert rq.headers["Content-Type"] == "text/csv"
        assert b'host,ip,port,ssl,errors\r\n,localhost,443,,-\r\n' in rq.content
        assert rq.status_code == 200
