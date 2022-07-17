from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


def encode_uid(id: int) -> str:
    return force_str(urlsafe_base64_encode(force_bytes(id)))


def decode_uid(id: int) -> str:
    return force_str(urlsafe_base64_decode(id))


def get_site_url(request: HttpRequest) -> str:
    site = get_current_site(request)
    domain = site.domain
    protocol = "https" if request.is_secure else "http"
    return f"{protocol}://{domain}"
