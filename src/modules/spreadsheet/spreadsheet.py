import os

from google.oauth2.service_account import Credentials
import gspread


class SpreadSheet:
    def __init__(self):
        # 認証
        self.credential_file_path = os.environ["GCP_CREDENTIAL_FILEPATH"]
        self.spreadsheet_url = os.environ["SPREADSHEET_URL"]
        self.scopes = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive",
        ]
        self.credentials = Credentials.from_service_account_file(
            self.credential_file_path, scopes=self.scopes
        )
        self.gc = gspread.authorize(self.credentials)

    def open_by_url(self, spreadsheet_url: str):
        spreadsheet = self.gc.open_by_url(spreadsheet_url)
        return spreadsheet
