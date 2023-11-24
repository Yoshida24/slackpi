import time

from PIL import Image

import requests
import io
import base64

DESIRED_SIZE = 64


def get_device_port() -> str:
    return "80"


def get_device_ip_address() -> str:
    """IPアドレスを返却

    Returns:
        str: "192.168.179.26"
    """
    res = requests.post("https://app.divoom-gz.com/Device/ReturnSameLANDevice")
    # {"ReturnCode":0,"ReturnMessage":"","DeviceList":[{"DeviceName":"Pixoo64","DeviceId":300055181,"DevicePrivateIP":"192.168.179.26","DeviceMac":"c4dee2233270","Hardware":90}]}
    return res.json()["DeviceList"][0]["DevicePrivateIP"]


def base_url() -> str:
    return f"http://{get_device_ip_address()}:{get_device_port()}"


def display_text(text: str):
    requests.post(
        f"{base_url()}/post",
        json={
            "Command": "Draw/SendHttpText",
            "TextId": 1,
            "x": 0,
            "y": 42,
            "dir": 0,
            "font": 4,
            "TextWidth": 56,
            "speed": 10,
            "TextString": text,
            "color": "#FFFFFF",
            "align": 1,
        },
    )


def url_to_rgb_base64(image_url: str):
    # URLから画像データを取得
    response = requests.get(image_url)
    if response.status_code == 200:
        # BytesIOを使用して画像データを読み込み
        image_data = io.BytesIO(response.content)

        # PILで画像を開きRGBモードに変換
        with Image.open(image_data) as img:
            # アンチエイリアシングを使用してリサイズ
            img = img.resize((DESIRED_SIZE, DESIRED_SIZE), Image.Resampling.LANCZOS)

            # 軽いぼかし効果を適用（オプション）
            # img = img.filter(ImageFilter.GaussianBlur(1))

            img = img.convert("RGB")

            # 画像の各ピクセルからRGB値を取得
            width, height = img.size
            rgb_values = []
            for y in range(height):
                for x in range(width):
                    r, g, b = img.getpixel((x, y))
                    rgb_values.append(f"{r:02x}{g:02x}{b:02x}")

            # RGB値を空白で区切った文字列に変換
            rgb_str = " ".join(rgb_values)

            # RGB文字列をバイト配列に変換してBase64エンコード
            rgb_bytes = bytes.fromhex(rgb_str.replace(" ", ""))
            return base64.b64encode(rgb_bytes).decode()
    else:
        raise Exception("Image could not be retrieved from the URL.")


def reset():
    requests.post(
        f"{base_url()}/post",
        json={"Command": "Draw/ResetHttpGifId"},
    )

    requests.post(
        f"{base_url()}/post",
        json={"Command": "Draw/ClearHttpText"},
    )


def display(image_url: str | None, text: str | None):
    """URL・文字列を与えると画像と文字列を表示

    Args:
        image_url (str | None): 画像のURL e.g. "https://komori541milk.web.fc2.com/dot/1Kanto/137n.png"
        text (str | None): 表示するテキスト
    """
    if image_url is not None or text is not None:
        reset()

    if image_url is not None:
        encoded_rgb_data = url_to_rgb_base64(image_url)
        requests.post(
            f"{base_url()}/post",
            json={
                "Command": "Draw/SendHttpGif",
                "PicNum": 1,
                "PicWidth": DESIRED_SIZE,
                "PicOffset": 0,
                "PicID": 1,
                "PicSpped": 200,
                "PicData": encoded_rgb_data,
            },
        )

    if text is not None:
        time.sleep(1)
        display_text(text=text)
