import pandas as pd
import streamlit as st

# 子スクリプトをインポート
# import net_income_chart
# import stock_and_income_chart
# import stock_chart

import chart4
import chart5
import chart6

st.set_page_config(page_title="日本株 投資判断", menu_items=None, layout="wide")
st.title("📈 日本株 株価・為替・純利益相関グラフ")

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


@st.cache_data(ttl=3600)
def load_data():
    return pd.read_csv("data.csv", encoding="shift-jis")


try:
    df = load_data()
    df["コード"] = df["コード"].astype(str)
except Exception as e:
    st.error(f"data.csv の読み込みに失敗しました: {e}")
    st.stop()

df["表示用"] = df["コード"] + " : " + df["銘柄名"]
selected_display = st.selectbox("銘柄を選択してください", df["表示用"])

if selected_display:
    selected_row = df[df["表示用"] == selected_display].iloc[0]
    selected_code = selected_row["コード"]
    name = selected_row["銘柄名"]

    st.subheader(f"📌 銘柄名: {name} (コード: {selected_code})")
    st.markdown("---")

    # --- 3つのタブで画面を切り替え ---
    tab1, tab2, tab3 = st.tabs(
        [
            "📈 株価 ＆ 為替レート",
            "📊 年間当期純利益 ＆ 為替レート",
            "📉 株価 ＆ 年間当期純利益",
        ]
    )

    with tab1:
        chart4.render(selected_code)

    with tab2:
        chart5.render(selected_code)

    with tab3:
        chart6.render(selected_code)

else:
    st.info("銘柄を選択してください。")