"""Defines the Slack Bolt application for interacting with medleys-love-notes-automation."""

import os

from dotenv import load_dotenv

from slack_bolt.adapter.fastapi import SlackRequestHandler
from slack_bolt.app import App

__all__ = ("app", "handler")

load_dotenv()

app = App(token=os.environ["SLACK_BOT_TOKEN"], signing_secret=os.environ["SLACK_SIGNING_SECRET"])
handler = SlackRequestHandler(app)


@app.command("/hello")
def hello(ack, say, command):
    ack()
    user_id = command["user_id"]
    say(f"Hello, <@{user_id}>! You sent the command: `{command['command']}` with text: `{command['text']}`")
