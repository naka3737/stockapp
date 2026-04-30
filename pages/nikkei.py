import streamlit as st
import pandas as pd
import yfinance as yf
from japaname import get_data

def main():

    st.set_page_config(page_title="日経平均寄与株", menu_items=None)
    st.title("日経平均寄与株")

    # 調べたい銘柄リスト

    codes = ["9983.T","6857.T", "8035.T","9984.T","6762.T","5803.T","4063.T","6954.T","9433.T","4519.T"]

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