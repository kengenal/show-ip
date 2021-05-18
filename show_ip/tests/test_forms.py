from django.core.files.uploadedfile import SimpleUploadedFile

from show_ip.forms import ShowIpForm
from show_ip.tests.base_test_case import BaseCSVTestCase


class TestShowIpForm(BaseCSVTestCase):
    def test_validate_empty_fields_should_be_return_validate_error(self):
        form = ShowIpForm(data={})

        assert not form.is_valid()
        assert "Field addresses or file cannot be empty" in form.errors["__all__"]

    def test_validate_with_only_address_type_should_be_return_array_elements(self):
        form = ShowIpForm(data={"addresses": "www.exmaple1.com:www.example2.com"})

        assert form.is_valid()
        assert not form.errors

    def test_validate_with_only_csv_file_should_be_return_array_elements(self, load_csv):
        with open(load_csv, 'rb') as file:
            form = ShowIpForm({}, {"file": SimpleUploadedFile(file.name, file.read())})
            check = form.is_valid()

            assert check
            assert form.cleaned_data["addresses"] is not None
            assert not form.errors

    def test_validate_with_only_csv_file_should_be_validate_errors(self, load_empty_csv):
        with open(load_empty_csv, 'rb') as file:
            form = ShowIpForm({}, {"file": SimpleUploadedFile(file.name, file.read())})

            assert not form.is_valid()
            assert "file" in form.errors

    def test_validate_with_wrong_file_extensions_should_be_return_validation_error(self, load_random_file):
        with open(load_random_file, 'rb') as file:
            form = ShowIpForm({}, {"file": SimpleUploadedFile(file.name, file.read())})

            assert not form.is_valid()
            assert "file" in form.errors
