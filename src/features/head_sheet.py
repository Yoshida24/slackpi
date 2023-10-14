import os

from modules.spreadsheet.spreadsheet import SpreadSheet
from slack_bolt import Say
from type.type import MessageEventHandlerArgs

def head_sheet(args: MessageEventHandlerArgs) -> None:
    spreadsheet_client = SpreadSheet()

    # SpreadSheetへ接続
    spreadsheet_url = os.environ["SPREADSHEET_URL"]
    spreadsheet = spreadsheet_client.open_by_url(spreadsheet_url)

    # 処理を実行
    sheet_values = spreadsheet.sheet1.get_all_values()
    # [['id', 'message'], ['1', 'Foo'], ['2', 'Bar']]
    message = f"A1の要素：{sheet_values[0][0]}\nSpreadSheet URL: {spreadsheet_url}"

    args.say(text=message)
