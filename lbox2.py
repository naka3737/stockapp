import streamlit as st
import yfinance as yf
import pandas as pd

def listmake2():

    # 1. CSVファイルを読み込む
    # ※ファイルパスは自分の環境に合わせて変更してください
    df = pd.read_csv('data.csv', encoding='shift_jis')

    # 2. リストボックスに表示するためのラベルを作成する
    # 「コード」と「企業名」を合体させて、選択しやすくします
    #df['display_name'] = df['コード'].astype(str) + " " + df['銘柄名']
    
    df['表示名'] = df['コード'].astype(str) + " " + df['銘柄名']

    df_sorted = df.sort_values('銘柄名', ascending=True)

    # 3. リストボックス（selectbox）を表示
    st.title("銘柄一覧")

    selected_option = st.selectbox(
        "銘柄を選んでください",
        #df_sorted['銘柄名']
        df_sorted['表示名']
    )

    # 4. 選択された銘柄のコードだけを抽出して表示（後の処理で使いやすいように）
    selected_code = selected_option.split(" ")[0]

    return selected_code

    st.write(f"現在選択中のコード: **{selected_code}**")

