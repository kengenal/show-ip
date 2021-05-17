import socket
import ssl
from urllib.parse import urlparse


def generate(hostnames):
    for hostname in hostnames:
        yield get_cert(hostname)


def get_cert(url, port=443, timeout=None):
    """Retrieve server's certificate at the specified address (host, port)."""
    parse = urlparse(url)
    host = parse.netloc if parse.netloc else parse.path
    try:
        with socket.create_connection((host, port), timeout=timeout) as sock:
            rq = sock.getpeername()
            data = {"ip": rq[0], "port": rq[1], "host": host, "errors": []}
            try:
                context = ssl.create_default_context()
                with context.wrap_socket(sock, server_hostname=host) as sslsock:
                    sslsock.getpeercert()
            except ssl.SSLCertVerificationError as err:
                data["ssl"] = err
    except socket.gaierror:
        data = {"ip": None, "port": 443, "host": host, "errors": ["Website is not exists"]}
    return data
