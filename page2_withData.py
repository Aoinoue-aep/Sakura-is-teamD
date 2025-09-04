import streamlit as st
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials


def getData():
    # 認証情報の設定
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('sakurahackathon-1a44c616a5af.json', scope)

    # クライアントの作成
    client = gspread.authorize(creds)

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1mRJj0IyX9EZ8NvV75-BAC_imRyRkF1k7skJ5sRBRz7M"

    spreadsheet = client.open_by_url(spreadsheet_url)
    return spreadsheet.sheet1.get_all_values()

st.title('管理者用ページ')

df = pd.DataFrame(getData(), columns=["name", "value"])
print(df)

# DataFrameを表示
st.write(df)

#管理者用送信ボタンの処理
if st.button('シフト一括作成'):
    st.write('送信されました')