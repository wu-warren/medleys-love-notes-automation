"""Provides a command line interface for medleys-love-notes-automation."""

import argparse
import importlib.metadata

import uvicorn

from mlna.api import rest_api

__all__ = ("main",)


def main():
    """The main entrypoint."""

    PROJECT_NAME = "mlna"
    meta = importlib.metadata.metadata(PROJECT_NAME)
    parser = argparse.ArgumentParser(description=meta.get("Summary"))
    parser.add_argument("-v", "--version", action="version", version=importlib.metadata.version(PROJECT_NAME))
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host to bind the server",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Port to bind the server",
    )
    parser.add_argument(
        "--reload",
        action="store_true",
        help="Enable auto-reload",
    )
    args = parser.parse_args()

    uvicorn.run(
        rest_api,
        host=args.host,
        port=args.port,
        reload=args.reload,
    )
