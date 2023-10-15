from features.echo import echo
from features.echo_block import echo_block
from features.head_sheet import head_sheet
from type.type import RoutingConfig

route_config: list[RoutingConfig] = [
    RoutingConfig(
        command="echo",
        description="reply with user input.",
        args=["user_input"],
        options=[],
        handler=echo,
    ),
    RoutingConfig(
        command="echo_block",
        description="show block.",
        args=[],
        options=[],
        handler=echo_block,
    ),
    RoutingConfig(
        command="head_sheet",
        description="reply with spreadsheet data",
        args=[],
        options=[],
        handler=head_sheet,
    ),
]
