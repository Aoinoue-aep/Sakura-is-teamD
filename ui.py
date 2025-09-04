import streamlit as st
from google.oauth2.service_account import Credentials
import gspread

st.title('プロトタイプ')

SERVICE_ACCOUNT_FILE = "sakurahakkathon-2cb4c8b89c18.json"  # Jsonキー
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# JSON キーを使って認証情報を作成
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

# gspread に認証情報を渡す
gc = gspread.authorize(creds)

#スプレッドシートに入力する情報
SPREADSHEET_ID = "1mRJj0IyX9EZ8NvV75-BAC_imRyRkF1k7skJ5sRBRz7M"
SHEET_NAME = "シート1"

sheet = gc.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)


st.header('従業員用ページ')

name = st.text_input("名前")
text=input = st.text_input('希望日を入力してください')

if st.button("送信"):
    if not name or not text:
        st.warning("名前と希望日を入力してください")
    else:
        sheet.append_row([name, "".join(text)])
        st.success("送信完了！")

