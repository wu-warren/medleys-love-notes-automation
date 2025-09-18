"""Defines the APIs for interacting with medleys-love-notes-automation."""

from fastapi import FastAPI

rest_api_v1 = FastAPI(root_path="/api/v1")


@rest_api_v1.get("/")
def root():
    return {"status": "All systems operational"}
