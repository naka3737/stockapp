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
        ticker = yf.Ticker(selected_code)

# 現在株価の取得（fast_infoが取れない場合のフォールバックとしてhistoryも活用可能ですがそのまま維持）
        cprice = int(ticker.fast_info.last_price)
        st.metric(label="現在株価", value=f"{cprice} ドル")

        # 余裕を持たせた期間でデータを取得（週末を挟んでも十分な営業日数を確保するため '1mo' や '10d' 推奨）
        df = ticker.history(period="10d")
        past_prices = df[["Close"]].iloc[-5:]

        # データが十分に取得できているか確認
        if len(df) >= 5:
            # 後ろからのインデックスを安全に取得
            # price4 = df["Close"].iloc[-1]  # 最新（前日または当日）
            # df["Close"] の最後尾が有効な値（NaN以外）かチェック
            if not df.empty and pd.notna(df["Close"].iloc[-1]):
                price4 = df["Close"].iloc[-1]
            else:
            # iloc[-1] が取得できない場合のフォールバック（fast_infoを使用、または0など）
                try:
                    price4 = ticker.fast_info.last_price
                except Exception:
                    price4 = 0  # どちらもダメな場合のデフォルト値
            price5 = df["Close"].iloc[-2]  # 1日前
            price6 = df["Close"].iloc[-3]  # 2日前
            price7 = df["Close"].iloc[-4]  # 3日前
            price8 = df["Close"].iloc[-5]  # 4日前

            # st.write(price4)
            # st.write(price5)
        else:
            # データが少ない場合のフォールバック処理
            st.warning("十分な過去データが取得できませんでした。")
            # 必要に応じたデフォルト値や代替処理を記述


        price3 = ticker.fast_info.previous_close
        st.metric(label="前日株価", value=f"{int(price3)} ドル")
        # st.metric(label="前日株価", value=f"{int(price4)} 円")
        rate = (cprice - price3)/price3 * 100
        st.metric(label="前日比", value=f"{rate:.2f} ％")

        price52h = ticker.info["fiftyTwoWeekHigh"]
        st.metric(label="52週高値", value=f"{int(price52h)} ドル")

        price52l = ticker.info["fiftyTwoWeekLow"]
        st.metric(label="52週安値", value=f"{int(price52l)} ドル")

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
        
        # st.dataframe(
        #     past_prices,
        #     column_config={
        #         "終値": st.column_config.NumberColumn(
        #             "終値",
        #             width="small",  # 幅を小さく指定（"small", "medium", "large" などが選べます）
        #             format="%.1fドル" # ついでに「◯◯円」と綺麗に単位をつけることも可能です
        #         )
        #     },
        #     use_container_width=False # 画面いっぱいに横に広がるのを防ぐ
        # )
        past_prices_df = pd.DataFrame(
            {
                "終値": [price4, price5, price6, price7, price8],
            },
        index=[
        "最新",
        "1日前",
        "2日前",
        "3日前",
        "4日前",
            ],  # 必要に応じて日付の文字列やラベルに変更可能
        )

    # 2. 欠損値を直前の値で埋める安全策
    past_prices_df["終値"] = past_prices_df["終値"].ffill()

    # 3. Streamlitで表示
    st.dataframe(
        past_prices_df,
        column_config={
            "終値": st.column_config.NumberColumn(
                "終値", width="small", format="%.1fドル"
            )
        },
        use_container_width=False,
    )