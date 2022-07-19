from abc import ABC
from typing import TypeVar

import requests
from bs4 import BeautifulSoup
from django.http import HttpRequest

from user.models import User

T = TypeVar("T")


class BaseService:
    def __init__(self, user: User):
        self.user = user
        self.model = None

    @classmethod
    def build_from_request(cls: T, request: HttpRequest) -> T:
        user = request.user if request.user and not request.user.is_anonymous else None
        return cls(user)


class BaseParser(ABC):
    def __init__(self, url: str) -> None:
        self.url = url
        self.page = ""
        self.soup = None

    def get_page(self) -> None:
        try:
            response = requests.get(self.url)
            self.page = response.text
        except Exception as e:
            print(f"Error fetching the URL: {self.url}")
            print(e)

    def make_soup(self) -> None:
        try:
            self.soup = BeautifulSoup(self.page, "lxml")
        except Exception as e:
            print(f"Cannot parse the page: {self.url}")
            print(e)

    def parse(self):
        self.get_page()
        self.make_soup()
