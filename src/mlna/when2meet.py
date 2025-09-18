"""Provides a when2meet interface."""

import pandas as pd


def get_availability(url: str) -> pd.DataFrame:
    """Get members' availability."""
    raise NotImplementedError
