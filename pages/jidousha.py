import streamlit as st
import pandas as pd
import yfinance as yf
from japaname import get_data

def main():

    st.set_page_config(page_title="自動車株", menu_items=None)
    st.title("自動車株")

    # 調べたい銘柄リスト

    codes = ["7203.T","7267.T", "7201.T","7261.T","7211.T","7269.T","7202.T"]

    with st.spinner('データを取得中...'):

        # yf.downloadで一括取得（高速化）
        df = yf.download(codes, period="2d")

        # 画面を横に分割（銘柄ごとにカードを並べる）
        #cols = st.columns(len(codes))

        for i, code in enumerate(codes):

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

            
        print(df.tail())

    # 下に詳細な表も表示してみる
    st.subheader("詳細データ")
    st.dataframe(df['Close'].tail())

main()

if st.button("戻る"):
    st.switch_page("mainpage.py")