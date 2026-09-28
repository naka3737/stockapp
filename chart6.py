import altair as alt
import pandas as pd
import streamlit as st
import yfinance as yf


def render(selected_code):
    st.write(f"### 📉 株価 ＆ 年間当期純利益の比較（過去4年間）")

    ticker_symbol = f"{selected_code}.T"

    with st.spinner("株価データおよび年間財務データを取得中..."):
        try:
            stock = yf.Ticker(ticker_symbol)

            # 1. 株価データの取得（過去4年分）
            hist_df = stock.history(period="4y")

            # 2. 年間当期純利益データの取得
            fin_df = stock.financials
            income_df = pd.DataFrame()

            if fin_df is not None and not fin_df.empty:
                net_income_row = None
                for row_name in [
                    "Net Income",
                    "Net Income Common Stockholders",
                    "Net Income From Continuing Operation",
                ]:
                    if row_name in fin_df.index:
                        net_income_row = row_name
                        break

                if net_income_row:
                    income_series = fin_df.loc[net_income_row].dropna()
                    income_df = pd.DataFrame({"Net_Income": income_series})
                    income_df.index = pd.to_datetime(
                        income_df.index
                    ).normalize()
                    income_df["Net_Income_億円"] = (
                        income_df["Net_Income"] / 100000000
                    )

            if not hist_df.empty:
                hist_df.index = hist_df.index.tz_localize(None).normalize()
                stock_chart_df = hist_df.reset_index()[["Date", "Close"]].rename(
                    columns={"Close": "Stock_Close"}
                )

                # 左軸：株価（線グラフ）
                line_stock = (
                    alt.Chart(stock_chart_df)
                    .mark_line(color="#1f77b4")
                    .encode(
                        x=alt.X(
                            "Date:T",
                            title="日付",
                            axis=alt.Axis(format="%Y-%m-%d"),
                        ),
                        y=alt.Y(
                            "Stock_Close:Q",
                            title="株価 (円)",
                            axis=alt.Axis(titleColor="#1f77b4"),
                        ),
                        tooltip=[
                            alt.Tooltip("Date:T", title="日付", format="%Y-%m-%d"),
                            alt.Tooltip(
                                "Stock_Close:Q", title="株価", format=",.2f"
                            ),
                        ],
                    )
                )

                charts_to_layer = [line_stock]

                # 右軸：年間当期純利益（棒グラフ）
                if not income_df.empty:
                    income_chart_df = income_df.reset_index().rename(
                        columns={income_df.index.name or "index": "Date"}
                    )

                    bar_income = (
                        alt.Chart(income_chart_df)
                        .mark_bar(color="#2ca02c", opacity=0.7, width=30)
                        .encode(
                            x=alt.X("Date:T", title="日付 / 決算期"),
                            y=alt.Y(
                                "Net_Income_億円:Q",
                                title="年間当期純利益 (億円)",
                                axis=alt.Axis(
                                    titleColor="#2ca02c", orient="right"
                                ),
                            ),
                            tooltip=[
                                alt.Tooltip(
                                    "Date:T",
                                    title="決算期",
                                    format="%Y-%m-%d",
                                ),
                                alt.Tooltip(
                                    "Net_Income_億円:Q",
                                    title="年間当期純利益 (億円)",
                                    format=",.2f",
                                ),
                            ],
                        )
                    )
                    charts_to_layer.append(bar_income)

                    combined_chart = (
                        alt.layer(*charts_to_layer)
                        .resolve_scale(y="independent")
                        .interactive()
                    )
                else:
                    combined_chart = line_stock.interactive()
                    st.warning(
                        "※年間当期純利益データが取得できなかったため、株価のみ表示します。"
                    )

                st.altair_chart(combined_chart, use_container_width=True)

                st.markdown(
                    '<span style="color:#1f77b4;">■</span> **株価（左軸・青線）** ｜ '
                    '<span style="color:#2ca02c;">■</span> **年間当期純利益（右軸・緑色棒グラフ）**',
                    unsafe_allow_html=True,
                )

                with st.expander("詳細な年間財務データを見る"):
                    if not income_df.empty:
                        st.dataframe(income_df[["Net_Income_億円"]])
                    else:
                        st.write("データなし")
            else:
                st.warning("株価データの取得に失敗しました。")
        except Exception as e:
            st.error(f"データの取得・描画中にエラーが発生しました: {e}")