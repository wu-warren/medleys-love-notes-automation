"""Provides a mocked when2meet interface."""

import pandas as pd

from mlna.mock.utils import resolve_path


def get_availability(url: str) -> pd.DataFrame:
    if url != "https://www.when2meet.com/?31478378-ueBAy":
        raise NotImplementedError(f"Invalid {url=} provided to mock when2meet interface")
    return pd.read_csv(resolve_path("when2meet.csv"))
