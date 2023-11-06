from io import BytesIO
from playwright.sync_api import sync_playwright


def take_screenshot(url: str, **kwargs) -> dict:
    # BytesIOオブジェクトを作成します
    output = BytesIO()
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        screenshot = page.screenshot(full_page=True)
        output.write(screenshot)
        browser.close()

    return {"message": "screen shot saved.", "file": output}


screenshot_function = {
    "name": "take_screenshot",
    "description": "Save screenshot of web page.",
    "parameters": {
        "type": "object",
        "properties": {
            "url": {
                "type": "string",
                "description": "URL to take screenshot. e.g. https://www.google.com/",
            },
        },
    },
}
