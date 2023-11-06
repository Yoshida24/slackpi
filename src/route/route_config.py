import features.echo as echo
import features.echo_block as echo_block
import features.head_sheet as head_sheet
import features.llm_chatbot.llm_chatbot as llm_chatbot
from type.type import CommandRoutingConfig, UnstructuredMessageRoutingConfig
from dataclasses import dataclass


@dataclass
class RouteConfig:
    command_routing_configs: list[CommandRoutingConfig]
    unstructured_message_routing_config: UnstructuredMessageRoutingConfig


route_config: RouteConfig = RouteConfig(
    command_routing_configs=[
        CommandRoutingConfig(
            command="echo",
            description="reply with user input.",
            args=["user_input"],
            options=[],
            handler=echo.handler,
        ),
        CommandRoutingConfig(
            command="echo_block",
            description="show block.",
            args=[],
            options=[],
            handler=echo_block.handler,
        ),
        CommandRoutingConfig(
            command="head_sheet",
            description="reply with spreadsheet data",
            args=[],
            options=[],
            handler=head_sheet.handler,
        ),
    ],
    unstructured_message_routing_config=UnstructuredMessageRoutingConfig(
        description="reply with user input.",
        handler=llm_chatbot.handler,
    ),
)
