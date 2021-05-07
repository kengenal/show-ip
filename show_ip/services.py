import socket
import ssl
from urllib.parse import urlparse


def generate(hostnames):
    for hostname in hostnames:
        yield get_cert(hostname)


def get_cert(url, port=443, timeout=None):
    """Retrieve server's certificate at the specified address (host, port)."""
    parse = urlparse(url)
    host = parse.path if parse.path else parse.netloc
    with socket.create_connection((host, port), timeout=timeout) as sock:
        rq = sock.getpeername()
        data = {"ip": rq[0], "port": rq[1]}
        try:
            context = ssl.create_default_context()
            with context.wrap_socket(sock, server_hostname=host) as sslsock:
                return sslsock.getpeercert()
        except ssl.SSLCertVerificationError as err:
            data["ssl"] = err
    return data
