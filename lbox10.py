import streamlit as st
import yfinance as yf
import pandas as pd

def listmake(df):

# display_name がまだ作られていない場合を考慮して、ここでも作れるようにしておく
    if "display_name" not in df.columns:
        df["display_name"] = df["Symbol"].astype(str) + " " + df["Company"]

    # セレクトボックスを表示
    selected_display = st.selectbox("銘柄を選択してください", df["display_name"])

    # 選択された display_name から「Symbol（コード）」だけを抜き出して返す
    #（スペースで分割して最初の部分を取得）
    if selected_display:
        selected_code = selected_display.split(" ")[0]
        return selected_code

    return None

    st.write(f"現在選択中のコード: **{selected_code}**")

