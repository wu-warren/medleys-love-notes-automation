"""Provides a command line interface for medleys-love-notes-automation."""

import argparse
import importlib.metadata


__all__ = ("main",)


def main():
    """The main entrypoint."""

    PROJECT_NAME = "mlna"
    PROJECT_SCRIPT = "mlna-cli"

    meta = importlib.metadata.metadata(PROJECT_NAME)
    parser = argparse.ArgumentParser(prog=PROJECT_SCRIPT, description=meta.get("Summary"))
    parser.add_argument("-v", "--version", action="version", version=importlib.metadata.version(PROJECT_NAME))
    args = parser.parse_args()
    print("TODO: parse arguments", vars(args))
