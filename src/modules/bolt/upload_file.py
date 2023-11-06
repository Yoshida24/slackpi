from slack_bolt import App
from type.type import MentionBody
from typing import Any
from slack_sdk.errors import SlackApiError


def upload_file(
    app: App,
    mention_body: MentionBody,
    file,
    thread_ts: str,
    filename="screenshot.png",
    title="Screenshot",
):
    try:
        file.seek(0)  # Ensure we're at the start of the file
        result = app.client.files_upload_v2(
            channels=mention_body.event.channel,
            thread_ts=thread_ts,
            file=file,
            filename=filename,
            title=title,
        )
        return result["file"]  # the uploaded file
    except SlackApiError as e:
        print(f"Error uploading file: {e}")
