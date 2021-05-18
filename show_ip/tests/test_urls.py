from django.urls import resolve, reverse


def test_show_ip_urls():
    assert reverse("show:ip") == "/en/"
    assert resolve("/en/").view_name == "show:ip"
