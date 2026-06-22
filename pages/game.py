import streamlit as st
import pandas as pd
import yfinance as yf
from japaname import get_data

def main():

    st.set_page_config(page_title="ゲーム株", menu_items=None)
    st.title("ゲーム株")

    # 調べたい銘柄リスト

    codes = ["7974.T","6758.T","9697.T", "9684.T", "6460.T","7832.T","9766.T","3635.T","7803.T","3632.T","3668.T","3656.T","2432.T","2121.T","3765.T"]

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