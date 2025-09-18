"""Utilities for interacting with the mock implementation."""

import importlib.resources
from importlib.resources.abc import Traversable

__all__ = ("resolve_path",)


PROJECT_NAME = "mlna"


def resolve_path(filename: str) -> Traversable:
    """Resolve a given filename into the full filepath of a given resource."""
    return importlib.resources.files(PROJECT_NAME).joinpath("mock", "data", filename)
