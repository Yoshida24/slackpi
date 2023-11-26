from slack_bolt import App
from slack_sdk.web.slack_response import SlackResponse
from type.type import MentionBody
from typing import Any, Optional


def get_conversations(
    app: App,
    mention_body: MentionBody,
) -> SlackResponse:
    res: SlackResponse = app.client.conversations_replies(
        channel=mention_body.event.channel,
        ts=mention_body.event.thread_ts
        if mention_body.event.thread_ts is not None
        else mention_body.event.ts,
    )
    return res
