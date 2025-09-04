import streamlit as st
import pandas as pd

st.title('管理者用ページ')

# ダミーデータの作成
df = pd.read_csv("sample.csv", encoding="utf_8")

# DataFrameを表示
st.write(df)

#管理者用送信ボタンの処理
if st.button('シフト一括作成'):
    st.write('送信されました')