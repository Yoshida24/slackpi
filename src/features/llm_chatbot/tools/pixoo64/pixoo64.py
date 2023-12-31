import time

from PIL import Image

import requests
import io
import base64

DISPLAY_WIDTH = 64
DISPLAY_HEIGHT = 64
DESIRED_SIZE = 64
pos_def = {"bottom": 47, "middle": 24, "top": 1}


def get_device_port() -> str:
    return "80"


def get_device_ip_address() -> str:
    """IPアドレスを返却

    Returns:
        str: "192.168.179.26"
    """
    res = requests.post("https://app.divoom-gz.com/Device/ReturnSameLANDevice").json()
    # {"ReturnCode":0,"ReturnMessage":"","DeviceList":[{"DeviceName":"Pixoo64","DeviceId":300055181,"DevicePrivateIP":"192.168.179.26","DeviceMac":"c4dee2233270","Hardware":90}]}
    if len(res["DeviceList"]) == 0:
        print("Pixoo64: Device not found. failed to get IP address")
        raise Exception("Pixoo64: Device not found. failed to get IP address")

    return res.json()["DeviceList"][0]["DevicePrivateIP"]


def get_device_ip_address_fixed() -> str:
    return "192.168.179.26"


def base_url() -> str:
    try:
        return f"http://{get_device_ip_address()}:{get_device_port()}"
    except Exception as e:
        return f"http://{get_device_ip_address_fixed()}:{get_device_port()}"


def display_text(
    text: str,
    color: str,
    pos: str,
):
    requests.post(
        f"{base_url()}/post",
        json={
            "Command": "Draw/SendHttpText",
            "TextId": 1,
            "x": 0,
            "y": pos_def[pos],
            "dir": 0,
            "font": 4,
            "TextWidth": DISPLAY_WIDTH,
            "speed": 5,
            "TextString": text,
            "color": color,
            "align": 1,
        },
    )


def url_to_rgb_base64(image_url: str):
    """
    URLから画像データを取得し、RGB値をBase64エンコードして返却
    横長・縦長の画像の場合は短辺に合わせて中央を正方形にクリッピングする

        Args:
            image_url (str): _description_

        Raises:
            Exception: _description_

        Returns:
            _type_: _description_
    """
    response = requests.get(image_url)
    if response.status_code == 200:
        # BytesIOを使用して画像データを読み込み
        image_data = io.BytesIO(response.content)

        # PILで画像を開きRGBモードに変換
        with Image.open(image_data) as img:
            # 画像の中心部分を正方形にクリッピング
            width, height = img.size
            if width != height:
                min_dim = min(width, height)
                left = int((width - min_dim) / 2)
                top = int((height - min_dim) / 2)
                right = int((width + min_dim) / 2)
                bottom = int((height + min_dim) / 2)
                img = img.crop((left, top, right, bottom))

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


def display(
    image_url: str | None,
    text: str | None,
    text_color: str,
    text_pos: str,
):
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
        display_text(text=text, color=text_color, pos=text_pos)
