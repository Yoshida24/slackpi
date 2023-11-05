from slack_bolt import App
from type.type import MentionBody
from typing import Any
from slack_sdk.web.slack_response import SlackResponse


def update_message(
    app: App,
    channel: str,
    ts: str,
    text: str,
    blocks: list[dict[Any, Any]] = [],
) -> SlackResponse:
    res = app.client.chat_update(
        channel=channel,
        ts=ts,
        text=text,
        blocks=blocks,
    )
    return res
