import json

import requests
from .pixoo64 import display
from openai.types.chat import ChatCompletionToolParam


def pixoo64_display_image_text_impl(
    image_url: str | None = None, text: str | None = None, **kwargs
):
    display(image_url=image_url, text=text)
    return {"message": "success", "file": None}


pixoo64_display_image_text_tool: ChatCompletionToolParam = {
    "type": "function",
    "function": {
        "name": "pixoo64_display_image_text",
        "description": "Display image in URL to Pixoo, which is electronic billboard.",
        "parameters": {
            "type": "object",
            "properties": {
                "image_url": {
                    "type": "string",
                    "description": "Image URL. e.g. https://komori541milk.web.fc2.com/dot/4Shinnoh/474n.png",
                },
                "text": {
                    "type": "string",
                    "description": "Text to display on electronic billboard. e.g. hello world!",
                },
            },
            "required": [],
        },
    },
}
