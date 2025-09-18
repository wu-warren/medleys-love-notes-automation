import pytest

from mlna.when2meet import get_availability


def test_get_availability():
    with pytest.raises(NotImplementedError):
        get_availability("https://www.when2meet.com/?31478378-ueBAy")
