from io import BytesIO
from playwright.sync_api import sync_playwright


def save_screenshot(url, output):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        page.goto(url)
        screenshot = page.screenshot()
        output.write(screenshot)
        browser.close()


def take_screenshot(name: str, **kwargs) -> str:
    # 使用例:
    # スクリーンショットを保存するURLと出力先ファイル名を指定します
    url = "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/back/female/25.png"
    output_file = "screenshot.png"

    # BytesIOオブジェクトを作成します
    output = BytesIO()

    # スクリーンショットを保存します
    save_screenshot(url, output)

    # BytesIOからファイルに書き込みます
    with open(output_file, "wb") as file:
        file.write(output.getvalue())

    return "screen shot saved."


screenshot_function = {
    "name": "take_screenshot",
    "description": "Save screenshot of pokemon.",
    "parameters": {
        "type": "object",
        "properties": {
            "name": {
                "type": "string",
                "description": "Pokemon name, e.g. pikachu",
            },
        },
    },
}
