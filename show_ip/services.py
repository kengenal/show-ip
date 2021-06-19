import socket
import ssl

from urllib.parse import urlparse
from django.utils.translation import gettext_lazy as _
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError


def generate(hostnames):
    for hostname in hostnames:
        yield get_cert(hostname.strip())


def get_cert(url, port=443, timeout=None):
    """Retrieve server's certificate at the specified address (host, port)."""
    parse = urlparse(url)
    host = parse.netloc if parse.netloc else parse.path
    data = {"ip": None, "port": 443, "host": host}
    try:
        validate = URLValidator()
        validate(f"https://{host}")
        with socket.create_connection((host, port), timeout=timeout) as sock:
            rq = sock.getpeername()
            data = {"ip": rq[0], "port": rq[1], "host": host}
            try:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=host) as sslsock:
                    sslsock.getpeercert()
            except ssl.SSLCertVerificationError as err:
                data["ssl"] = err
    except ValidationError:
        data["error"] = _("Incorrect url address")
    except (socket.gaierror, OSError):
        data["error"] = _("Website is not exists")
    return data
