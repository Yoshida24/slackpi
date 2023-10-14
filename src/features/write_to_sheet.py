import os

from google.oauth2.service_account import Credentials
import gspread

# 認証
credential_file_path = os.environ['GCP_CREDENTIAL_FILEPATH']
spreadsheet_url =  os.environ['SPREADSHEET_URL']
scopes = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]
credentials = Credentials.from_service_account_file(
    credential_file_path,
    scopes=scopes
)
gc = gspread.authorize(credentials)

# SpreadSheetへ接続
spreadsheet = gc.open_by_url(spreadsheet_url)

# シートの書き込み（Update）を実行
# - 一度全データ消去を行ってから書き込みを行う
# - ワークシートがなければ作る
worksheet_name = 'write3'
try:
    worksheet = spreadsheet.worksheet(worksheet_name)
    worksheet.clear()
except Exception as e:
    worksheet = spreadsheet.add_worksheet(worksheet_name, rows=100, cols=26)

worksheet.append_rows(values=[['id', 'message'], ['3', 'foobar']] , table_range='A1')
print('OK: worksheet is ' + worksheet.url)
