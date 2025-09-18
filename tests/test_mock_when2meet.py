import pytest

from datetime import datetime

from mlna.mock.when2meet import get_availability


def is_valid_datetime(datetime_string: str) -> bool:
    """Check if the string is a valid datetime"""
    try:
        datetime.strptime(datetime_string, "%a %b %d %H:%M:%S %Y")
        return True
    except ValueError:
        return False


def test_get_availability_invalid():
    with pytest.raises(Exception):
        get_availability("https://www.when2meet.com/?invalid")


def test_get_availability_mock():
    availability_df = get_availability("https://www.when2meet.com/?31478378-ueBAy")
    for column in availability_df.columns:
        assert column == "Unnamed: 0" or "Aug" in column and is_valid_datetime(column)
