import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from route.route import listen_message, listen_action
from modules.bolt.listener import message_definitions
from modules.bolt.listener import action_definitions
from modules.spreadsheet import spreadsheet


if __name__ == "__main__":
    slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
    slack_app_token = os.environ["SLACK_APP_TOKEN"]
    message_defs = message_definitions(spreadsheet.fetch_message_definitions)
    action_defs = action_definitions(spreadsheet.fetch_action_definitions)
    app = App(token=slack_bot_token)

    listen_message(app=app)
    listen_action(app=app, action_defs=action_defs)

    SocketModeHandler(app, slack_app_token).start()
