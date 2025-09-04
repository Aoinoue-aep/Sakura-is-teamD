import gspread
from oauth2client.service_account import ServiceAccountCredentials

# 認証情報の設定
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name('sakurahackathon-1a44c616a5af.json', scope)

# クライアントの作成
client = gspread.authorize(creds)

"""# スプレッドシートの取得
spreadsheet = client.open('年越しアニクラ')

# ワークシートの取得
worksheet = spreadsheet.sheet1
"""

spreadsheet_url = "https://docs.google.com/spreadsheets/d/1Ag7kLUHZHAfwkcIfTCwkI4xqEPatp2PHIppye40GGOc"

spreadsheet = client.open_by_url(spreadsheet_url)
print(spreadsheet.sheet1.get_all_values())