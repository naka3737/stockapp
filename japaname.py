import streamlit as st
import pandas as pd
import yfinance as yf

@st.cache_data # これを入れると読み込みが爆速になります
def load_data():
    return pd.read_csv("data.csv", encoding='shift-jis')

df = load_data()
df['コード'] = df['コード'].astype(str)

def get_data(cname):

# タイトル
#st.title("日本株 配当利回りチェッカー")

# 1. ユーザーからの入力（数字だけを想定）
#user_input = st.text_input("証券コードを入力してください", "", placeholder="例: 7203")

    if cname:
        # 1. まず自前のリスト(df)から日本語名を探す
        result = df[df['コード'] == cname]
        
        if not result.empty:
            # 日本語名が見つかった場合
            cname = result.iloc[0]['銘柄名']
        else:
            # 見つからなかった場合は「不明」とする
            cname = "不明な銘柄"

    return cname