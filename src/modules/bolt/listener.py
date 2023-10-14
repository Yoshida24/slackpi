from dataclasses import dataclass
from typing import Callable


# MessageDef
@dataclass
class MessageTrigger:
    handler_id: str
    keyword: str


@dataclass
class MessageDef:
    id: str
    blocks: list[dict]
    triggers: list[MessageTrigger]


def message_definitions(query: Callable[[], list[MessageDef]]) -> list[MessageDef]:
    return query()


# ActionDef
@dataclass
class ActionDef:
    id: str
    text: str


def action_definitions(query: Callable[[], list[ActionDef]]) -> list[ActionDef]:
    return query()
