import streamlit as st
import pandas as pd
import yfinance as yf
from lbox8 import listmake 

st.set_page_config(page_title="株主優待", menu_items=None)
# ページのタイトル
st.title("🎁株主優待")

# 最大表示行数と列数の制限を「なし（None）」に設定する
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None) # 横幅の自動折り返しを防ぐ


# 1. データの読み込み
@st.cache_data(ttl=3600) # これを入れると読み込みが爆速になります
def load_data():
    return pd.read_csv("yutai3.csv", encoding='shift-jis')

df = load_data()
df['code'] = df['code'].astype(str)


    # 2. 検索ボックスを表示
    #user_input = st.text_input("証券コードを入力してください（例: 7203）", "")

#user_input = st.selectbox("銘柄を選択してください", df['コード'])

selected_code = listmake()
print(selected_code)

#if user_input:
    # 3. 検索処理
result = df[df['code'] == selected_code]

print(result)

if not result.empty:
    name = result.iloc[0]['銘柄名']
    st.subheader(f"📌 銘柄名: {name}")

    naiyou = result.iloc[0]['優待内容']
    kingaku = result.iloc[0]['優待金額換算']

    st.metric(label="優待内容", value=f"{naiyou} 　{kingaku}円")

    kenribi = result.iloc[0]['優待月']

    st.metric(label="優待権利日", value=f"{kenribi} ")

    yutai_url = f"https://finance.yahoo.co.jp/quote/{selected_code}.T/incentive"

    st.link_button("🎁 この銘柄の優待詳細をチェック", yutai_url)

    # 4. 株価取得
    with st.spinner('株価を取得中...'):
        ticker = yf.Ticker(f"{selected_code}.T")
        price = ticker.fast_info.last_price

        # 投資判断（推奨）を表示
        #handan = ticker.recommendations

        # 配当利回り (0.03 = 3% のように小数で入っています)
        dividend_yield = ticker.info.get('dividendYield')
        # 1株あたりの年間配当額
        dividend_rate = ticker.info.get('dividendRate')
        if dividend_yield is not None:
            st.metric(label="配当利回り", value=f"{dividend_yield:.2f} %")
            st.metric(label="1株配当（年間）", value=f"{dividend_rate} 円")
        else:
            st.metric(label="配当利回り", value="データなし")

        st.metric(label="現在株価", value=f"{int(price)} 円")
else:
    st.error("そのコードは銘柄リストにありません。")


    # except Exception as e:
    #     st.error(f"エラーが発生しました。data.csv があるか確認してください。")