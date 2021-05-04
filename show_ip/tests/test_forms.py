import csv
import os

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile

from show_ip.forms import ShowIpForm


class TestShowIpForm:
    @pytest.fixture()
    def load_csv(self):
        path = os.path.abspath('test.csv')
        with open(path, mode='w') as employee_file:
            employee_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            employee_writer.writerow(["www.example.com", "tak"])
            employee_writer.writerow(["www.example2.com"])
        yield path
        os.remove(path)

    def test_validate_empty_fields_should_be_return_validate_error(self):
        form = ShowIpForm(data={})

        assert not form.is_valid()

    def test_validate_with_only_address_type_should_be_return_array_elements(self):
        form = ShowIpForm(data={"addresses": "www.exmaple1.com:www.example2.com"})

        assert form.is_valid()

    def test_validate_with_only_csv_file_should_be_return_array_elements(self, load_csv):
        with open(load_csv, 'rb') as file:
            form = ShowIpForm({}, {"file": SimpleUploadedFile(file.name,file.read())})
            check = form.is_valid()

            assert check
            assert form.cleaned_data["addresses"] is not None
