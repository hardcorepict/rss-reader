from abc import ABC
from datetime import datetime, timezone
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
    def __init__(self, url: str, parser: str = "lxml") -> None:
        self.url = url
        self.page = ""
        self.soup = None
        self.parser = parser

    def get_page(self) -> None:
        try:
            response = requests.get(self.url)
            self.page = response.text
        except Exception as e:
            print(f"Error fetching the URL: {self.url}")
            print(e)

    def make_soup(self) -> None:
        try:
            self.soup = BeautifulSoup(self.page, self.parser)
        except Exception as e:
            print(f"Cannot parse the page: {self.url}")
            print(e)

    def parse(self):
        self.get_page()
        self.make_soup()


class DatetimeService:
    RFC_822_FORMATS = ["%a, %d %b %Y %H:%M:%S %z", "%a, %d %b %Y %H:%M:%S %Z"]

    def from_str(self, string: str) -> datetime:
        date = None

        for format in self.RFC_822_FORMATS:
            try:
                date = datetime.strptime(string, format)
            except ValueError:
                pass

        if date is None:
            raise ValueError("Invalid date format")

        return date

    def to_utc(self, date: datetime) -> datetime:
        return date.astimezone(timezone.utc)
