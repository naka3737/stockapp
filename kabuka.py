import pandas as pd
import requests
import streamlit as st
import yfinance as yf
import datetime
from bs4 import BeautifulSoup
from sector import csector

def kabuka(selected_code):
    # 4. 株価取得
    with st.spinner("株価を取得中..."):
        ticker = yf.Ticker(f"{selected_code}.T")



        cprice = int(ticker.fast_info.last_price)
        st.metric(label="現在株価", value=f"{cprice} 円")

        df = ticker.history(period="7d")
        past_prices = df[["Close"]].iloc[-6:-1]

        price4 = df["Close"].iloc[-1]      # 前日
        price5 = df["Close"].iloc[-2]      # 前々日
        price6 = df["Close"].iloc[-3]    # 前々々日
        price7 = df["Close"].iloc[-4]    # 前々々々日
        price8 = df["Close"].iloc[-5]    # 前々々々々日



        price3 = ticker.fast_info.previous_close
        st.metric(label="前日株価", value=f"{int(price3)} 円")
        # st.metric(label="前日株価", value=f"{int(price4)} 円")
        rate = (cprice - price3)/price3 * 100
        st.metric(label="前日比", value=f"{rate:.2f} ％")

        if price4 < price5 and price5 < price6:
            if price6 < price7:
                if price7 < price8:
                    st.metric(label="連続下落", value=f"株価が４日連続で下落しています")
                else:
                    st.metric(label="連続下落", value=f"株価が３日連続で下落しています")
            # else:
            #     st.metric(label="連続下落", value=f"株価が３日連続で下落しています")

        if price4 > price5 and price5 > price6:
            if price6 > price7:
                if price7 > price8:
                    st.metric(label="連続上昇", value=f"株価が４日連続で上昇しています")
                else:
                    st.metric(label="連続上昇", value=f"株価が３日連続で上昇しています")
            # else:
            #     st.metric(label="連続上昇", value=f"株価が３日連続で上昇しています")

        past_prices = past_prices.iloc[::-1]
        past_prices = past_prices.rename(columns={"Close": "終値"})

        # インデックスを日付のみに変換
        past_prices.index = past_prices.index.strftime('%Y-%m-%d')
        past_prices.index.name = ""

        # タイトル
        st.write("### 直近の株価一覧 (1日前〜5日前)")
        # st.write(past_prices)
        
        st.dataframe(
            past_prices,
            column_config={
                "終値": st.column_config.NumberColumn(
                    "終値",
                    width="small",  # 幅を小さく指定（"small", "medium", "large" などが選べます）
                    format="%.1f円" # ついでに「◯◯円」と綺麗に単位をつけることも可能です
                )
            },
            use_container_width=False # 画面いっぱいに横に広がるのを防ぐ
        )