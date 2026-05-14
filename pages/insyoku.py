import streamlit as st
import pandas as pd
import yfinance as yf
from japaname import get_data

def main():

    st.set_page_config(page_title="飲食業株", menu_items=None)
    st.title("飲食業株")

    # 調べたい銘柄リスト

    codes = ["3197.T","7550.T", "7616.T","2702.T","7581.T","3387.T","7412.T","2695.T","7421.T","2705.T","3563.T"]

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