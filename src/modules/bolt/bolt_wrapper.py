import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


class BoltWrapper:
    def __init__(self, listen):
        self.slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
        self.slack_app_token = os.environ["SLACK_APP_TOKEN"]
        self.app = App(token=self.slack_bot_token)
        self.listen = listen

    def start(self):
        self.listen(app=self.app)
        SocketModeHandler(self.app, self.slack_app_token).start()
