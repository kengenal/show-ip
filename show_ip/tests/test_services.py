import pytest

from show_ip.services import get_cert


@pytest.mark.skip(
    reason="this tests should be run only local testing or debugging because test needs communicate with another server"
)
class TestCert:
    def test_cert_with_wrong_host_name_should_be_return_dict_with_errors_key_and_ip_should_be_none(self):
        cert = get_cert("33333")

        assert cert["ip"] is None
        assert "error" in cert

    def test_get_cert_with_correct_address_but_host_not_exists_should_be_return_dict_with_errors_key(self):
        cert = get_cert("23123123123123.com")

        assert cert["ip"] is None
        assert "error" in cert

    def test_gert_with_correct_ip_should_be_return_ip_and_ssl_key_should_be_not_exists(self):
        cert = get_cert("google.com")

        assert "ssl" not in cert
        assert cert["ip"] is not None
