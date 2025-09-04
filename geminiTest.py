from google import genai
from google.genai import types
import gspread
from oauth2client.service_account import ServiceAccountCredentials

client = genai.Client(api_key="AIzaSyAHp94iPLAJ1Cw27Dw_fWQKR3niYfkFAsI")

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
    creds = ServiceAccountCredentials.from_json_keyfile_name('sakurahackathon-1a44c616a5af.json', scope)

    # クライアントの作成
    client = gspread.authorize(creds)

    spreadsheet_url = "https://docs.google.com/spreadsheets/d/1mRJj0IyX9EZ8NvV75-BAC_imRyRkF1k7skJ5sRBRz7M"

    spreadsheet = client.open_by_url(spreadsheet_url)
    return spreadsheet.sheet1.get_all_values()


with open("systemInst.txt", "r", encoding="utf-8") as f:
    sys_ins = f.read()

# ここでmain_promptとスプシから持ってきたデータをドッキング
main_prompt = str(getData())

print(gemini(main_prompt, sys_ins))