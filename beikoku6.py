import pandas as pd
import streamlit as st
import yfinance as yf
from supabase import create_client, Client
from lbox10 import listmake
from sector import csector

# ==========================================
# Supabase 接続設定
# ==========================================
SUPABASE_URL = "https://aryfiqxqhxgzjrthmvfw.supabase.co"
SUPABASE_KEY = "sb_publishable_kVkKwid4tWg5iW9kQyasmg_B8k249K5"  # ←ご自身のキーに書き換えてください
TABLE_NAME = "russell"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ページのタイトル
st.title("📈 米国株 投資判断（Supabase連携版）")

# 最大表示行数と列数の制限を「なし（None）」に設定する
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)


# 1. Supabaseからデータを読み込む関数
def load_data():
    # Supabaseのテーブルから全データ（全行）を取得
    response = supabase.table(TABLE_NAME).select("*").order("idx", desc=False).execute()
    df = pd.DataFrame(response.data)
    
    if df.empty:
        return df

    df["Symbol"] = df["Symbol"].astype(str)

    if "idx" in df.columns:
        df["idx"] = df["idx"].astype(str).str.zfill(4)
    
    # PFフィールドの空白（NoneやNaN）を空文字に統一
    if "PF" in df.columns:
        df["PF"] = df["PF"].fillna("")
    else:
        df["PF"] = ""
        
    return df


df = load_data()

if df.empty:
    st.error("Supabaseからデータを取得できませんでした。接続やテーブル名を確認してください。")
else:
    # ==========================================
    # PFフィールド（y）を使った絞り込み処理
    # ==========================================
    show_pf_only = st.checkbox("⭐ ポートフォリオ（PF）登録銘柄のみ表示する")

    if show_pf_only:
        # PF列が「y」の銘柄だけを抽出
        df = df[df["PF"] == "y"]
        if df.empty:
            st.info("ポートフォリオに登録されている銘柄がありません。先に銘柄を追加してください。")

    # ==========================================
    # 2. 検索ボックスを表示
    # ==========================================
    selected_code = listmake(df)
    print(selected_code)

    # 3. 検索処理（最新の状態を反映するため再取得）
    df_original = load_data()
    result = df_original[df_original["Symbol"] == selected_code]
    print(result)

    if not result.empty:
        name = result.iloc[0]["Company"]
        sector = result.iloc[0]["GICS Sector"]
        sname = csector(sector)
        subsector = result.iloc[0]["GICS Sub-Industry"]
        st.subheader(f"📌 銘柄名: {name} \n\n{sname} \n\n{subsector}")

        # 現在選択されている銘柄のPF状態を取得
        current_pf_status = result.iloc[0]["PF"]

        # ==========================================
        # Supabaseへ保存する ポートフォリオ追加 / 削除 ボタン
        # ==========================================
        col1, col2 = st.columns([1, 4])
        with col1:
            if current_pf_status == "y":
                # すでに「y」の場合は「外す」ボタン
                if st.button("⭐ PFから外す", key="remove_pf"):
                    # Supabaseの該当レコードを更新（PFを空文字にする）
                    supabase.table(TABLE_NAME).update({"PF": ""}).eq("Symbol", selected_code).execute()
                    st.success("ポートフォリオから削除しました！")
                    st.rerun()
            else:
                # 空白の場合は「追加」ボタン
                if st.button("➕ PFに追加", key="add_pf"):
                    # Supabaseの該当レコードを更新（PFに「y」を入れる）
                    supabase.table(TABLE_NAME).update({"PF": "y"}).eq("Symbol", selected_code).execute()
                    st.success("ポートフォリオに追加しました！")
                    st.rerun()

        if current_pf_status == "y":
            st.caption("※この銘柄はポートフォリオに登録されています。")
        # ==========================================

        # 4. 株価取得
        with st.spinner("株価を取得中..."):
            ticker = yf.Ticker(f"{selected_code}")

            cprice = ticker.fast_info.last_price
            st.metric(label="現在株価", value=f"{cprice:.2f} ドル")

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

            try:
                handan = ticker.recommendations
                if handan is not None and not handan.empty:
                    st.write(handan)
                else:
                    st.write("現在、推奨データは利用できません。")
            except Exception:
                st.write("推奨データの取得中にエラーが発生しました。")

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

                st.metric(label="最新の強気(Strong Buy)評価数", value=f"{latest['strongBuy']}件")
                st.metric(label="最新の買い(Buy)評価数", value=f"{latest['buy']}件")
                st.metric(label="最新の中立(hold)評価数", value=f"{latest['hold']}件")
                st.metric(label="最新の売り(sell)評価数", value=f"{latest['sell']}件")
                st.metric(label="最新の弱気(Strong Sell)評価数", value=f"{latest['strongSell']}件")
                st.metric(label="総評価数", value=f"{goukei}件")

                price2 = ticker.fast_info.last_price

                if handan2 is not None:
                    st.metric(label="目標株価", value=f"{int(handan2)} ドル")
                    kairi = (int(handan2) - int(price2)) / int(price2) * 100
                    st.metric(label="現在株価", value=f"{int(price2)} ドル")
                    st.metric(label="乖離率", value=f"{int(kairi)} %")
                    if kairi < 0:
                        st.warning("⚠️ 現在の株価が目標株価を上回っています（割高の可能性があります）。")
                else:
                    st.metric(label="目標株価", value="データなし")
                    st.metric(label="現在株価", value=f"{int(price2)} ドル")

            else:
                st.metric(label="投資判断", value="データがありません")
                price2 = ticker.fast_info.last_price
                st.metric(label="現在株価", value=f"{int(price2)} ドル")
    else:
        st.error("そのコードは銘柄リストにありません。")