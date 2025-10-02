"""Defines the Slack Bolt application for interacting with medleys-love-notes-automation."""

import os

from dotenv import load_dotenv

from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.async_app import AsyncApp

__all__ = ("app", "handler")

load_dotenv()

app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])
handler = SlackRequestHandler(app)


@app.command("/hello")
async def hello(ack, say, command):
    await ack()
    user_id = command["user_id"]
    await say(f"Hello, <@{user_id}>! You sent the command: `{command['command']}` with text: `{command['text']}`")
