from slack_bolt import App
from type.type import MentionBody
from typing import Any


def reply(
    app: App, mention_body: MentionBody, text: str, blocks: list[dict[Any, Any]] = []
):
    app.client.chat_postMessage(
        channel=mention_body.event.channel,
        text=text,
        blocks=blocks,
        thread_ts=mention_body.event.thread_ts
        if mention_body.event.thread_ts is not None
        else mention_body.event.ts,
    )
