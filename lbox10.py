import streamlit as st
import yfinance as yf
import pandas as pd

def listmake(df):
    # 表示用の「display_name」を作る（インデックス + Symbol + Company の結合）
    if "display_name" not in df.columns:
        df["display_name"] = (
            df["idx"].astype(str).str.zfill(4)
            + " "
            + df["Symbol"].astype(str)
            + " "
            + df["Company"]
        )

    # セレクトボックスを表示
    selected_display = st.selectbox("銘柄を選択してください", df["display_name"])

    if selected_display:
        # 【修正】選ばれた display_name と完全に一致する行を df から探す
        matched_rows = df[df["display_name"] == selected_display]

        if not matched_rows.empty:
            # 一致した行の 'Symbol' をそのまま返す（これなら絶対にズレません）
            selected_code = matched_rows.iloc[0]["Symbol"]
            return selected_code

    return None

    st.write(f"現在選択中のコード: **{selected_code}**")

