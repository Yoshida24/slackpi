from dataclasses import dataclass
from typing import Callable, Optional
from slack_bolt import App
from typing import Any
from slack_sdk.web.slack_response import SlackResponse


@dataclass
class MentionEvent:
    blocks: list[dict]
    channel: str = ""
    client_msg_id: str = ""
    event_ts: str = ""
    parent_user_id: Optional[str] = None
    team: str = ""
    text: str = ""
    thread_ts: Optional[str] = None
    ts: str = ""
    type: str = ""
    user: str = ""
    attachments: Optional[Any] = None
    files: Optional[Any] = None


@dataclass
class MentionBody:
    token: str
    team_id: str
    api_app_id: str
    event: MentionEvent
    type: str
    event_id: str
    event_time: int
    authorizations: list[dict]
    is_ext_shared_channel: bool
    event_context: str


@dataclass
class MentionEventHandlerArgs:
    args: Any
    event: MentionBody
    app: App
    messages: Optional[Any] = None


@dataclass
class CommandRoutingConfig:
    command: str
    description: str
    args: list[str]
    options: list[str]
    handler: Callable[[MentionEventHandlerArgs], None]


@dataclass
class UnstructuredMessageRoutingConfig:
    description: str
    handler: Callable[[MentionEventHandlerArgs], None]
