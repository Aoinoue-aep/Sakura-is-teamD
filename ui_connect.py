import streamlit as st
from google.oauth2.service_account import Credentials
from oauth2client.service_account import ServiceAccountCredentials
import gspread
import pandas as pd
from google import genai
from google.genai import types
from io import StringIO

def gemini(prompt, sys):
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=sys),
    )
    return response.text

def getData():
    # 認証情報の設定
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name('sakurahakkathon-2cb4c8b89c18.json', scope)

    # クライアントの作成
    client = gspread.authorize(creds)

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1mRJj0IyX9EZ8NvV75-BAC_imRyRkF1k7skJ5sRBRz7M"

    spreadsheet = client.open_by_url(spreadsheet_url)
    return spreadsheet.sheet1.get_all_values()

# Gemini API キー
client = genai.Client(api_key="AIzaSyAHp94iPLAJ1Cw27Dw_fWQKR3niYfkFAsI")

# 主命令文
with open("systemInst.txt", "r", encoding="utf-8") as f:
    sys_ins = f.read()

# スプシから取得したみんなの希望文
main_prompt = str(getData())

if "page" not in st.session_state:
    st.session_state.page = "home"

@st.fragment
def go_to(page):
    st.session_state.page = page

if st.session_state.page == "home":
    st.title("シフト管理アプリ")
    st.write("利用するモードを選んでください")
    
    st.button("従業員", on_click=go_to("employee"))
    st.button("管理者用", on_click=go_to("admin"))
    
elif st.session_state.page == "employee":
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

            st.subheader("あなたが送信した内容")
            st.write(f"- 名前: {name}")
            st.write(f"- 内容: {text}")
            
            st.button("ホームに戻る", on_click=go_to("home"))

elif st.session_state.page == "admin":
    st.title('管理者用ページ')

    df = pd.DataFrame(getData(), columns=["name", "value"])

    # DataFrameを表示
    st.write(df)

    #管理者用送信ボタンの処理
    if st.button('シフト一括作成'):
        st.write('送信されました')
        csv_text = gemini(main_prompt, sys_ins)

        df = pd.read_csv(StringIO(csv_text))
        
        df["日付"] = df["日"].astype(str) + "(" + df["曜日"] + ")"

        df_melt = df.melt(id_vars=["日","日付"],  value_vars=["担当者1","担当者2","担当者3","担当者4","担当者5"],value_name="名前").drop(columns="variable")
        df_melt = df_melt.dropna(subset=["名前"])
        df_melt["シフト"] = "○"

        pivot_df = df_melt.pivot_table(
            index="名前", columns="日", values="シフト", aggfunc="first")

        pivot_df.columns = [
            df.set_index("日").loc[day, "日付"] for day in pivot_df.columns
        ]

        st.subheader("シフト表")
        st.dataframe(pivot_df.fillna(""))  
    
    st.button("ホームに戻る", on_click=go_to("home"))