import streamlit as st
import pandas as pd
import yfinance as yf
from japaname import get_data


st.set_page_config(page_title="資源株", menu_items=None)
st.title("資源株")

# 調べたい銘柄リスト

codes = ["CL=F","1671.T", "1690.T","2038.T","NG=F","1689.T"]

with st.spinner('データを取得中...'):

    # yf.downloadで一括取得（高速化）
    df = yf.download(codes, period="2d")

    # 画面を横に分割（銘柄ごとにカードを並べる）
    #cols = st.columns(len(codes))

    for i, code in enumerate(codes):
        if code == "CL=F":
            print("ok")
            # 原油（ドル表示）
            prev_close = df['Close'][code].iloc[0]
            last_price = df['Close'][code].iloc[-1]
            change_ratio = ((last_price - prev_close) / prev_close) * 100
            st.metric(
                label="WTI原油先物",
                value=f"{last_price:.1f} ドル",
                delta=f"{change_ratio:.2f}%"
            )
        elif code == "NG=F":
            # 天然ガス（ドル表示）
            prev_close = df['Close'][code].iloc[0]
            last_price = df['Close'][code].iloc[-1]
            change_ratio = ((last_price - prev_close) / prev_close) * 100
            st.metric(
                label="Henry Hub天然ガス先物",
                value=f"{last_price:.3f} ドル",
                delta=f"{change_ratio:.2f}%"
            )  
        else:
            jname = get_data(code.replace(".T", ""))
            prev_close = df['Close'][code].iloc[0]
            last_price = df['Close'][code].iloc[-1]
            change_ratio = ((last_price - prev_close) / prev_close) * 100
            
            # ブラウザ専用の綺麗な表示（ラベル, 現在値, 前日比）
            st.metric(
                label=f"{code} {jname}",
                value=f"{last_price:.1f} 円",
                delta=f"{change_ratio:.2f}%"
            )

# 下に詳細な表も表示してみる
st.subheader("詳細データ")
st.dataframe(df['Close'].tail())