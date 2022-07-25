from datetime import datetime, timedelta, timezone

import pytest
import pytz

from app.base.services import DatetimeService


class TestDatatimeService:
    service = DatetimeService()

    def test_from_str__when_first_pattern(self):
        date_str = "Wed, 02 Oct 2002 08:00:00 GMT"

        date = self.service.from_str(date_str)

        assert date.day == 2
        assert date.month == 10
        assert date.tzinfo is None

    def test_from_str__when_second_pattern(self):
        date_str = "Wed, 02 Oct 2002 13:00:00 +0300"

        date = self.service.from_str(date_str)

        assert date.day == 2
        assert date.month == 10
        assert date.tzinfo == timezone(timedelta(seconds=3 * 60 * 60))

    def test_from_str__when_wrong_pattern(self):
        date_str = "Wed, 02 Oct 2002 13:00:00"

        with pytest.raises(ValueError):
            date = self.service.from_str(date_str)

    def test_to_utc__when_already_utc(self):
        date = datetime(2022, 6, 23, 10, 11, 12, tzinfo=timezone.utc)

        new_date = self.service.to_utc(date)

        assert new_date.tzinfo == timezone.utc

    def test_to_utc(self):
        date = datetime(2022, 6, 23, 10, 11, 12, tzinfo=pytz.timezone("Europe/Minsk"))

        new_date = self.service.to_utc(date)

        assert new_date.tzinfo == timezone.utc
        assert new_date.hour == date.hour - 2
