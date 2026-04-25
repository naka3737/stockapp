import streamlit as st
import pandas as pd
import yfinance as yf
from japaname import get_data

st.set_page_config(page_title="銀行株", menu_items=None)
st.title("銀行株")

# 調べたい銘柄リスト

codes = ["8306.T","8411.T", "8316.T","8308.T","7182.T","8303.T","8304.T","5838.T","8410.T"]

with st.spinner('データを取得中...'):

    # yf.downloadで一括取得（高速化）
    df = yf.download(codes, period="2d")

    # 画面を横に分割（銘柄ごとにカードを並べる）
    cols = st.columns(len(codes))



    for i, code in enumerate(codes):
        jname = get_data(code.replace(".T", ""))
        #with cols[i]:
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