import streamlit as st
import pandas as pd
import yfinance as yf
from japaname import get_data

st.set_page_config(page_title="金属", menu_items=None)
st.title("金属")

# 調べたい銘柄リスト

codes = ["1540.T", "1541.T","1542.T","1543.T","1672.T","1692.T","1693.T"]

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

if st.button("戻る"):
    st.switch_page("mainpage.py")