
import ipaddress
import socket
from urllib.parse import urlparse


def validate_url(url: str) -> None:
    parsed_url = urlparse(url)

    # Only allow HTTP and HTTPS.
    if parsed_url.scheme not in {"http", "https"}:
        raise ValueError("Only HTTP and HTTPS URLs are supported.")

    # URL must contain a hostname.
    hostname = parsed_url.hostname

    if not hostname:
        raise ValueError("URL must contain a hostname.")

    hostname = hostname.lower()

    # Block localhost names.
    blocked_hostnames = {
        "localhost",
        "localhost.localdomain",
        "metadata.google.internal",
    }

    if hostname in blocked_hostnames:
        raise ValueError("Access to this hostname is not allowed.")

    # Resolve the hostname to IP addresses.
    try:
        addresses = socket.getaddrinfo(
            hostname,
            None,
            type=socket.SOCK_STREAM,
        )
    except socket.gaierror as exc:
        raise ValueError("Could not resolve hostname.") from exc

    for address in addresses:
        ip = ipaddress.ip_address(address[4][0])

        if (
            ip.is_private
            or ip.is_loopback
            or ip.is_link_local
            or ip.is_reserved
            or ip.is_multicast
            or ip.is_unspecified
        ):
            raise ValueError(
                "Access to private or non-public IP addresses is not allowed."
            )