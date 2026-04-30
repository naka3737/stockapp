import streamlit as st
import yfinance as yf
import pandas as pd

def listmake():

    # 1. CSVファイルを読み込む
    # ※ファイルパスは自分の環境に合わせて変更してください
    df = pd.read_csv('russell.csv')

    # 2. リストボックスに表示するためのラベルを作成する
    # 「コード」と「企業名」を合体させて、選択しやすくします
    df['display_name'] = df['Symbol'].astype(str) + " " + df['Company']

    # 3. リストボックス（selectbox）を表示
    st.title("銘柄一覧")

    selected_option = st.selectbox(
        "銘柄を選んでください",
        df['display_name']
    )

    # 4. 選択された銘柄のコードだけを抽出して表示（後の処理で使いやすいように）
    selected_code = selected_option.split(" ")[0]

    return selected_code

    st.write(f"現在選択中のコード: **{selected_code}**")

