import json
from unittest import mock

from django.urls import reverse
from django.utils.http import urlencode
from rest_framework.test import APIClient as DRFClient
from rest_framework_simplejwt.tokens import RefreshToken


class APIClient(DRFClient):
    def login(
        self,
        user=None,
        backend="rest_framework_simplejwt.authentication.JWTAuthentication",
    ):
        if user is None:
            return super().login()

        with mock.patch("django.contrib.auth.authenticate") as authenticate:
            user.backend = backend
            authenticate.return_value = user

            return super().login()


def get_response_content(response):
    content = json.loads(response.content.decode("utf8"))
    return content


def reverse_querystring(
    view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None
):
    base_url = reverse(
        view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app
    )
    if query_kwargs:
        return "{}?{}".format(base_url, urlencode(query_kwargs))
    return base_url


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {"refresh": str(refresh), "access": str(refresh.access_token)}
