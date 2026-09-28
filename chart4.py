import altair as alt
import pandas as pd
import streamlit as st
import yfinance as yf


def render(selected_code):
    period_option = st.radio(
        "表示期間を選択してください",
        ["1月", "1年", "2年", "5年", "10年"],
        index=3,
        horizontal=True,
        key="stock_period_radio",
    )

    period_mapping = {
        "1月": "1mo",
        "1年": "1y",
        "2年": "2y",
        "5年": "5y",
        "10年": "10y",
    }
    selected_period = period_mapping[period_option]

    st.write(f"### 📉 チャート分析（株価 ＆ 為替 / {period_option}）")

    ticker_symbol = f"{selected_code}.T"
    usdjpy = yf.Ticker("USDJPY=X")

    with st.spinner("株価と為替データを取得中..."):
        try:
            stock = yf.Ticker(ticker_symbol)
            hist_df = stock.history(period=selected_period)
            fx_df = usdjpy.history(period=selected_period)

            if not hist_df.empty and not fx_df.empty:
                hist_df.index = hist_df.index.tz_localize(None).normalize()
                fx_df.index = fx_df.index.tz_localize(None).normalize()

                combined_df = pd.DataFrame(
                    {"Stock_Close": hist_df["Close"], "FX_Close": fx_df["Close"]}
                ).dropna()

                chart_df = combined_df.reset_index()

                line_stock = (
                    alt.Chart(chart_df)
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

                line_fx = (
                    alt.Chart(chart_df)
                    .mark_line(color="#ff7f0e", strokeDash=[4, 4])
                    .encode(
                        x=alt.X("Date:T"),
                        y=alt.Y(
                            "FX_Close:Q",
                            title="ドル円為替 (円/ドル)",
                            scale=alt.Scale(domain=[90, 170]),
                            axis=alt.Axis(
                                titleColor="#ff7f0e",
                                orient="right",
                                values=list(range(90, 171, 5)),
                            ),
                        ),
                        tooltip=[
                            alt.Tooltip(
                                "FX_Close:Q", title="ドル円レート", format=",.2f"
                            ),
                        ],
                    )
                )

                dual_chart = (
                    alt.layer(line_stock, line_fx)
                    .resolve_scale(y="independent")
                    .interactive()
                )
                st.altair_chart(dual_chart, use_container_width=True)

                st.markdown(
                    '<span style="color:#1f77b4;">■</span> **株価（左軸・青線）** ｜ '
                    '<span style="color:#ff7f0e;">---</span> **ドル円為替（右軸・オレンジ破線）**',
                    unsafe_allow_html=True,
                )
                with st.expander("詳細な結合データを見る"):
                    st.dataframe(combined_df)
            else:
                st.warning("株価または為替データの取得に失敗しました。")
        except Exception as e:
            st.error(f"データの取得・描画中にエラーが発生しました: {e}")