import pytest

from app.core.security import validate_url


def test_public_url_is_allowed():
    validate_url("https://example.com")


@pytest.mark.parametrize(
    "url",
    [
        "http://localhost",
        "http://127.0.0.1",
        "http://192.168.1.1",
        "http://10.0.0.1",
        "http://172.16.0.1",
        "http://169.254.169.254",
        "ftp://example.com",
    ],
)
def test_unsafe_urls_are_rejected(url):
    with pytest.raises(ValueError):
        validate_url(url)