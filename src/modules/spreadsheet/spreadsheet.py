from ..bolt.listener import ActionDef, MessageDef, MessageTrigger


def fetch_message_definitions() -> list[MessageDef]:
    return [
        MessageDef(
            id="message_1",
            blocks=[
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "hello Hey there 👋 I'm TaskBot. I'm here to help you create and manage tasks in Slack.\nThere are two ways to quickly create tasks:",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*1️⃣ Use the `/task` command*. Type `/task` followed by a short description of your tasks and I'll ask for a due date (if applicable). Try it out by using the `/task` command in this channel.",
                    },
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*2️⃣ Use the _Create a Task_ action.* If you want to create a task from a message, select `Create a Task` in a message's context menu. Try it out by selecting the _Create a Task_ action for this message (shown below).",
                    },
                },
                {
                    "type": "image",
                    "title": {"type": "plain_text", "text": "image1", "emoji": True},
                    "image_url": "https://api.slack.com/img/blocks/bkb_template_images/onboardingComplex.jpg",
                    "alt_text": "image1",
                },
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "➕ To start tracking your team's tasks, *add me to a channel* and I'll introduce myself. I'm usually added to a team or project channel. Type `/invite @TaskBot` from the channel or pick a channel on the right.",
                    },
                    "accessory": {
                        "type": "static_select",
                        "placeholder": {
                            "type": "plain_text",
                            "text": "Select options",
                            "emoji": True,
                        },
                        "options": [
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "*this is plain_text text*",
                                    "emoji": True,
                                },
                                "value": "value-0",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "*this is plain_text text*",
                                    "emoji": True,
                                },
                                "value": "value-1",
                            },
                            {
                                "text": {
                                    "type": "plain_text",
                                    "text": "*this is plain_text text*",
                                    "emoji": True,
                                },
                                "value": "value-2",
                            },
                        ],
                        "action_id": "static_select-action",
                    },
                },
                {"type": "divider"},
                {
                    "type": "context",
                    "elements": [
                        {
                            "type": "mrkdwn",
                            "text": "👀 View all tasks with `/task list`\n❓Get help at any time with `/task help` or type *help* in a DM with me",
                        }
                    ],
                },
            ],
            triggers=[MessageTrigger(handler_id="message_1", keyword="hello")],
        ),
        MessageDef(
            id="message_2",
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": "Hi there!"},
                    "accessory": {
                        "type": "button",
                        "text": {"type": "plain_text", "text": "Click Me 2"},
                        "action_id": "button_click_2",
                    },
                }
            ],
            triggers=[MessageTrigger(handler_id="message_2", keyword="hi")],
        ),
    ]


def fetch_action_definitions() -> list[ActionDef]:
    return [
        ActionDef(id="value-0", text="<@U04TUT8RC3T> clicked the button 1"),
        ActionDef(id="value-1", text="<@U04TUT8RC3T> clicked the button 2"),
        ActionDef(id="value-3", text="<@U04TUT8RC3T> clicked the button 3"),
    ]
