import pandas as pd
import requests
import streamlit as st
import yfinance as yf
import datetime
from bs4 import BeautifulSoup
from lbox10 import listmake
from kabuka import kabuka
from sector import csector

# ページのタイトル
st.title("📈 日本株 信用売り判断")

# 最大表示行数と列数の制限を「なし（None）」に設定する
pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)  # 横幅の自動折り返しを防ぐ


# 1. データの読み込み
def load_data():
    df = pd.read_csv("karauri.csv")
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
    df = df[df["PF"] == "y"]
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
    sector = result.iloc[0]["Section"]
    sname = csector(sector)
    # subsector =result.iloc[0]["GICS Sub-Industry"]
    st.subheader(f"📌 銘柄名: {name} \n\n{sname}")

    # 現在選択されている銘柄のPF状態を取得
    current_pf_status = result.iloc[0]["PF"]

    # ==========================================
    # CSVへ保存する ポートフォリオ追加 / 削除 ボタン
    # ==========================================
    col1, col2 = st.columns([1, 4])
    with col1:
        if current_pf_status == "y":
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
                    "y"
                )
                # CSVファイルに上書き保存
                df_original.to_csv("karauri.csv", index=False)
                st.success("ポートフォリオに追加しました！")
                st.rerun()

    if current_pf_status == "y":
        st.caption("※この銘柄はポートフォリオに登録されています。")
    # ==========================================

    profile_url2 = f"https://finance.yahoo.co.jp/quote/{selected_code}"
    st.link_button("🎁 この銘柄の企業情報をチェック", profile_url2)

    ticker = yf.Ticker(f"{selected_code}.T")

    price2 = ticker.fast_info.last_price
    st.metric(label="現在株価", value=f"{int(price2)} 円")

    kabuka(selected_code)

    st.write("バランスシート")

    total_debt = ticker.info.get("totalDebt")

    if total_debt is not None:
        # 数値なのでカンマ区切りにして表示
        st.metric(label="総負債", value=f"{total_debt:,} 円")
    else:
        # None などの場合は、エラーを防ぐために文字列で「データなし」などと表示
        st.metric(label="総負債", value="データなし")

    # net_debt = ticker.info.get("netlDebt")




    bs = ticker.balance_sheet

    try:
        # 総負債 と 現金 のデータを直接取得して引き算する
        # （※銘柄によって項目の名前が存在しない場合、ここでエラーになります）
        total_debt = bs.loc["Total Debt"].iloc[0]
        cash = bs.loc["Cash And Cash Equivalents"].iloc[0]

        net_debt = total_debt - cash

        st.metric(label="純負債", value=f"{net_debt:,.0f} 円")

        ratio = net_debt / total_debt

        ratio = ratio * 100

        # 小数点3桁まで表示（例: 0.250）
        st.metric(label="純負債 / 総負債比率", value=f"{ratio:.3f} %")

    except Exception:
        st.warning("この銘柄ではデータを取得・計算できませんでした。")


    op = ticker.info.get("operatingMargins")

    if op is not None:
    # 数値なのでカンマ区切りにして表示
        st.metric(label="売上高利益率",value =f" {op * 100: .2f}%")
    else:
    # None などの場合は、エラーを防ぐために文字列で「データなし」などと表示
        st.metric(label="売上高利益率", value="データなし")

    # if net_debt is not None:
    #     # 数値なのでカンマ区切りにして表示
    #     st.metric(label="純負債", value=f"{net_debt:,} 円")
    # else:
    #     # None などの場合は、エラーを防ぐために文字列で「データなし」などと表示
    #     st.metric(label="純負債", value="データなし")

    # st.metric(label="１日前株価", value=f"{int(price4)} 円")
    # st.metric(label="２日前株価", value=f"{int(price5)} 円")
    # st.metric(label="３日前株価", value=f"{int(price6)} 円")
    # st.metric(label="４日前株価", value=f"{int(price7)} 円")
    # st.metric(label="５日前株価", value=f"{int(price8)} 円")

    ex_div_timestamp = ticker.info.get("exDividendDate")

    if ex_div_timestamp:
        # 読みやすい日付形式（YYYY-MM-DD）に変換
        ex_div_date = datetime.datetime.fromtimestamp(ex_div_timestamp).strftime('%Y年%m月%d日')
        # st.write(f"直近の配当権利落ち日: {ex_div_date}")
        st.metric(label="直近の配当権利落ち日", value=f"{ex_div_date} ")
    else:
        # st.write("権利落ち日のデータが見つかりませんでした（無配当の銘柄など）")
        st.metric(label="直近の配当権利落ち日", value=f"見つかりませんでした")
    # 目標株価を表示
    handan2 = ticker.info.get("targetMeanPrice")

    # 配当利回り
    dividend_yield = ticker.info.get("dividendYield")
    dividend_rate = ticker.info.get("dividendRate")

    if dividend_yield is not None:
        yield_pct = dividend_yield
        st.metric(label="配当利回り", value=f"{yield_pct:.2f} %")
        st.metric(label="1株配当（年間）", value=f"{dividend_rate} 円")
    else:
        st.metric(label="配当利回り", value="データなし")

    try:
        handan = ticker.recommendations
        if handan is not None and not handan.empty:
            st.write(handan)
        else:
            st.write("現在、推奨データは利用できません。")
    except Exception:
        st.write("推奨データの取得中にエラーが発生しました。")

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
            st.metric(label="目標株価", value=f"{int(handan2)} 円")
            kairi = (int(handan2) - int(price2)) / int(price2) * 100
            st.metric(label="現在株価", value=f"{int(price2)} 円")
            st.metric(label="乖離率", value=f"{int(kairi)} %")
            if kairi < 0:
                st.warning(
                    "⚠️ 現在の株価が目標株価を上回っています（割高の可能性があります）。"
                )
        else:
            st.metric(label="目標株価", value=f"データなし")
            st.metric(label="現在株価", value=f"{int(price2)} 円")

    else:
        st.metric(label="投資判断", value="データがありません")
        # price2 = ticker.fast_info.last_price
        # st.metric(label="現在株価", value=f"{int(price2)} 円")
else:
    st.error("そのコードは銘柄リストにありません。")