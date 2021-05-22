from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from main.settings import base

urlpatterns = i18n_patterns(
    path("", include("show_ip.urls"))
) + static(base.STATIC_URL, document_root=base.STATIC_ROOT)
