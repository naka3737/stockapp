import pandas as pd
import requests
import streamlit as st
import yfinance as yf
from bs4 import BeautifulSoup
from lbox10 import listmake
from sector import csector

# ページのタイトル
st.title("📈 米国株 投資判断")

# 最大表示行数と列数の制限を「なし（None）」に設定する
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)  # 横幅の自動折り返しを防ぐ


# 1. データの読み込み
def load_data():
    df = pd.read_csv("russell.csv")
    df["Symbol"] = df["Symbol"].astype(str)

    if "idx" in df.columns:
        df["idx"] = df["idx"].astype(str).str.zfill(4)
    # 既存のPFフィールドの空白（NaN）を空文字に統一して処理しやすくする
    if "PF" in df.columns:
        df["PF"] = df["PF"].fillna("")
    else:
        df["PF"] = ""  # 万が一列名が違った場合の保険
    return df


df = load_data()

# ==========================================
# CSVのPFフィールド（〇）を使った絞り込み処理
# ==========================================
show_pf_only = st.checkbox("⭐ ポートフォリオ（PF）登録銘柄のみ表示する")

if show_pf_only:
    # PF列が「〇」の銘柄だけを抽出
    df = df[df["PF"] == "〇"]
    if df.empty:
        st.info(
            "ポートフォリオに登録されている銘柄がありません。先に銘柄を追加してください。"
        )

# ==========================================
# 2. 検索ボックスを表示 (lbox7.py に df を渡す)
# ==========================================
selected_code = listmake(df)
print(selected_code)

# 3. 検索処理 (ボタンを押した後に全データへ反映・保存させるため、元のcsvを基準にします)
df_original = load_data()
result = df_original[df_original["Symbol"] == selected_code]
print(result)

if not result.empty:
    name = result.iloc[0]["Company"]
    sector = result.iloc[0]["GICS Sector"]
    sname = csector(sector)
    st.subheader(f"📌 銘柄名: {name} {sname}")

    # 現在選択されている銘柄のPF状態を取得
    current_pf_status = result.iloc[0]["PF"]

    # ==========================================
    # CSVへ保存する ポートフォリオ追加 / 削除 ボタン
    # ==========================================
    col1, col2 = st.columns([1, 4])
    with col1:
        if current_pf_status == "〇":
            # すでに「〇」の場合は「外す」ボタン
            if st.button("⭐ PFから外す", key="remove_pf"):
                # 該当銘柄のPFを空にする
                df_original.loc[df_original["Symbol"] == selected_code, "PF"] = (
                    ""
                )
                # CSVファイルに上書き保存
                df_original.to_csv("russell.csv", index=False)
                st.success("ポートフォリオから削除しました！")
                st.rerun()
        else:
            # 空白の場合は「追加」ボタン
            if st.button("➕ PFに追加", key="add_pf"):
                # 該当銘柄のPFに「〇」を入れる
                df_original.loc[df_original["Symbol"] == selected_code, "PF"] = (
                    "〇"
                )
                # CSVファイルに上書き保存
                df_original.to_csv("russell.csv", index=False)
                st.success("ポートフォリオに追加しました！")
                st.rerun()

    if current_pf_status == "〇":
        st.caption("※この銘柄はポートフォリオに登録されています。")
    # ==========================================

    # 4. 株価取得
    with st.spinner("株価を取得中..."):
        ticker = yf.Ticker(f"{selected_code}")

        try:
            handan = ticker.recommendations
            if handan is not None and not handan.empty:
                st.write(handan)
            else:
                st.write("現在、推奨データは利用できません。")
        except Exception:
            st.write("推奨データの取得中にエラーが発生しました。")

        # 目標株価を表示
        handan2 = ticker.info.get("targetMeanPrice")

        # 配当利回り
        dividend_yield = ticker.info.get("dividendYield")
        dividend_rate = ticker.info.get("dividendRate")

        if dividend_yield is not None:
            yield_pct = dividend_yield
            st.metric(label="配当利回り", value=f"{yield_pct:.2f} %")
            st.metric(label="1株配当（年間）", value=f"{dividend_rate} ドル")
        else:
            st.metric(label="配当利回り", value="データなし")

        profile_url = f"https://finance.yahoo.com/quote/{selected_code}/profile"
        st.link_button("🎁 この銘柄の企業情報をチェック", profile_url)

        profile_url2 = f"https://finance.yahoo.co.jp/quote/{selected_code}"
        st.link_button("🎁 この銘柄の日本語企業情報をチェック", profile_url2)

        print(handan)
        print(handan2)

        recs = ticker.recommendations

        if recs is not None and not recs.empty:
            latest = recs.iloc[-1]
            goukei = (
                latest["strongBuy"]
                + latest["buy"]
                + latest["hold"]
                + latest["sell"]
                + latest["strongSell"]
            )

            st.metric(
                label="最新の強気(Strong Buy)評価数", value=f"{latest['strongBuy']}件"
            )
            st.metric(label="最新の買い(Buy)評価数", value=f"{latest['buy']}件")
            st.metric(label="最新の中立(hold)評価数", value=f"{latest['hold']}件")
            st.metric(label="最新の売り(sell)評価数", value=f"{latest['sell']}件")
            st.metric(
                label="最新の弱気(Strong Sell)評価数",
                value=f"{latest['strongSell']}件",
            )
            st.metric(label="総評価数", value=f"{goukei}件")

            price2 = ticker.fast_info.last_price

            if handan2 is not None:
                st.metric(label="目標株価", value=f"{int(handan2)} ドル")
                kairi = (int(handan2) - int(price2)) / int(price2) * 100
                st.metric(label="現在株価", value=f"{int(price2)} ドル")
                st.metric(label="乖離率", value=f"{int(kairi)} %")
                if kairi < 0:
                    st.warning(
                        "⚠️ 現在の株価が目標株価を上回っています（割高の可能性があります）。"
                    )
            else:
                st.metric(label="目標株価", value=f"データなし")
                st.metric(label="現在株価", value=f"{int(price2)} ドル")

        else:
            st.metric(label="投資判断", value="データがありません")
            price2 = ticker.fast_info.last_price
            st.metric(label="現在株価", value=f"{int(price2)} ドル")
else:
    st.error("そのコードは銘柄リストにありません。")