import os

from google.oauth2.service_account import Credentials
import gspread

from interfaces.types import SlackMessage


def read_from_sheet(event: SlackMessage, say):
    # 認証
    credential_file_path = os.environ["GCP_CREDENTIAL_FILEPATH"]
    spreadsheet_url = os.environ["SPREADSHEET_URL"]
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = Credentials.from_service_account_file(
        credential_file_path, scopes=scopes
    )
    gc = gspread.authorize(credentials)

    # SpreadSheetへ接続
    spreadsheet = gc.open_by_url(spreadsheet_url)

    # 処理を実行
    sheet_values = spreadsheet.sheet1.get_all_values()
    say(
        f"A1の要素：{sheet_values[0][0]}\nSpreadSheet URL: {spreadsheet_url}"
    )  # [['id', 'message'], ['1', 'Foo'], ['2', 'Bar']]
