import streamlit as st
import pandas as pd
import yfinance as yf
from lbox2 import listmake2 

# ページのタイトル
st.title("📈 日本株 投資判断")

# 最大表示行数と列数の制限を「なし（None）」に設定する
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None) # 横幅の自動折り返しを防ぐ


# 1. データの読み込み
@st.cache_data(ttl=3600) # これを入れると読み込みが爆速になります
def load_data():
    return pd.read_csv("data.csv", encoding='shift-jis')

df = load_data()
df['コード'] = df['コード'].astype(str)


    # 2. 検索ボックスを表示
    #user_input = st.text_input("証券コードを入力してください（例: 7203）", "")

#user_input = st.selectbox("銘柄を選択してください", df['コード'])

selected_code = listmake2()
print(selected_code)

#if user_input:
    # 3. 検索処理
result = df[df['コード'] == selected_code]

print(result)

if not result.empty:
    name = result.iloc[0]['銘柄名']
    st.subheader(f"📌 銘柄名: {name}")

    # 4. 株価取得
    with st.spinner('株価を取得中...'):
        ticker = yf.Ticker(f"{selected_code}.T")
        #price = ticker.fast_info.last_price

        # 投資判断（推奨）を表示
        handan = ticker.recommendations

        # 目標株価を表示
        handan2 = ticker.info.get("targetMeanPrice")

        # 配当利回り (0.03 = 3% のように小数で入っています)
        dividend_yield = ticker.info.get('dividendYield')
        # 1株あたりの年間配当額
        dividend_rate = ticker.info.get('dividendRate')

        if dividend_yield is not None:
            # 小数をパーセント表示に変換 (0.0345 -> 3.45%)
            yield_pct = dividend_yield 
            st.metric(label="配当利回り", value=f"{yield_pct:.2f} %")
            st.metric(label="1株配当（年間）", value=f"{dividend_rate} 円")
        else:
            st.metric(label="配当利回り", value="データなし")

        yutai_url = f"https://finance.yahoo.co.jp/quote/{selected_code}.T/incentive"

        st.link_button("🎁 この銘柄の優待情報をチェック", yutai_url)

        print(handan)

        print(handan2)

        recs = ticker.recommendations

        if recs is not None and not recs.empty:

            # 1. 一番下の行（最新月）だけを取得
            latest = recs.iloc[-1] 
            
            # 2. その中の「Strong Buy」や「Buy」の数字を取り出す
            # s_buy_count = latest['strongBuy']
            # buy_count = latest['buy']
            goukei = latest['strongBuy'] + latest['buy'] + latest['hold'] + latest['sell'] + latest['strongSell']
            
            # 3. st.metric で表示（ラベル, 値, 前月比などのデルタ）
            st.metric(label="最新の強気(Strong Buy)評価数", value=f"{latest['strongBuy']}件")
            st.metric(label="最新の買い(Buy)評価数", value=f"{latest['buy']}件")
            st.metric(label="最新の中立(hold)評価数", value=f"{latest['hold']}件")
            st.metric(label="最新の売り(sell)評価数", value=f"{latest['sell']}件")
            st.metric(label="最新の弱気(Strong Sell)評価数", value=f"{latest['strongSell']}件")

            st.metric(label="総評価数", value=f"{goukei}件")

            # price = ticker.fast_info.previous_close
            price2 = ticker.fast_info.last_price
            # ratio =  (ticker.fast_info.last_price - ticker.fast_info.previous_close) / ticker.fast_info.previous_close * 100

            # history_1mo = ticker.history(period="1mo")
            # history_1mo.index = history_1mo.index.strftime('%Y-%m-%d')
            # history_data = history_1mo[['Close']].sort_index(ascending=False)

            # high_price = history_1mo['High'].max()
            # high_date_raw = history_1mo['High'].idxmax() # ここで日付の場所を特定
            # high_date = high_date_raw.strftime('%Y-%m-%d') # ここで文字に変換
            # history_1mo.index = history_1mo.index.strftime('%Y-%m-%d')
            # st.metric(label="過去1か月の最高値", value=f"{high_price:.1f}円")
            # st.caption(f"記録日: {high_date}")

            # st.metric(label="過去1か月の最高値", value=f"{high_price:.1f}円")
            # st.caption(f"記録日: {high_date}")
            # st.dataframe(history_1mo[['Close']].sort_index(ascending=False))


            #st.dataframe(history_data)

            
            # 大きな数字で表示
            #st.metric(label="投資判断（推奨）", value=f"{handan} ")
            if handan2 is not None:
                st.metric(label="目標株価", value=f"{int(handan2)} 円")
                kairi = (int(handan2)-int(price2))/int(price2)*100
                st.metric(label="現在株価", value=f"{int(price2)} 円")
                st.metric(label="乖離率", value=f"{int(kairi)} %")
                if kairi < 0:
                    st.warning("⚠️ 現在の株価が目標株価を上回っています（割高の可能性があります）。")
            else:
                st.metric(label="目標株価", value=f"データなし") 
                st.metric(label="現在株価", value=f"{int(price2)} 円")



        else:
            st.metric(label="投資判断", value="データがありません")
            price2 = ticker.fast_info.last_price
            st.metric(label="現在株価", value=f"{int(price2)} 円")
else:
    st.error("そのコードは銘柄リストにありません。")


    # except Exception as e:
    #     st.error(f"エラーが発生しました。data.csv があるか確認してください。")