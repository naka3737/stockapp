import altair as alt
import pandas as pd
import streamlit as st
import yfinance as yf


def render(selected_code):
    st.write(f"### 📉 ドル円為替レート ＆ 年間当期純利益の比較（過去4年間）")

    ticker_symbol = f"{selected_code}.T"
    usdjpy = yf.Ticker("USDJPY=X")

    with st.spinner("為替データおよび年間財務データを取得中..."):
        try:
            stock = yf.Ticker(ticker_symbol)
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
                    income_df.index = pd.to_datetime(income_df.index).normalize()
                    income_df["Net_Income_億円"] = (
                        income_df["Net_Income"] / 100000000
                    )

            fx_df = usdjpy.history(period="4y")

            if not fx_df.empty:
                fx_df.index = fx_df.index.tz_localize(None).normalize()
                fx_chart_df = fx_df.reset_index()[["Date", "Close"]].rename(
                    columns={"Close": "FX_Close"}
                )

                line_fx = (
                    alt.Chart(fx_chart_df)
                    .mark_line(color="#ff7f0e")
                    .encode(
                        x=alt.X(
                            "Date:T",
                            title="日付",
                            axis=alt.Axis(format="%Y-%m-%d"),
                        ),
                        y=alt.Y(
                            "FX_Close:Q",
                            title="ドル円為替 (円/ドル)",
                            scale=alt.Scale(domain=[90, 170]),
                            axis=alt.Axis(titleColor="#ff7f0e"),
                        ),
                        tooltip=[
                            alt.Tooltip("Date:T", title="日付", format="%Y-%m-%d"),
                            alt.Tooltip(
                                "FX_Close:Q", title="ドル円レート", format=",.2f"
                            ),
                        ],
                    )
                )

                charts_to_layer = [line_fx]

                if not income_df.empty:
                    income_chart_df = income_df.reset_index().rename(
                        columns={income_df.index.name or "index": "Date"}
                    )

                    bar_income = (
                        alt.Chart(income_chart_df)
                        .mark_bar(color="#1f77b4", opacity=0.7, width=25)
                        .encode(
                            x=alt.X("Date:T", title="決算期（年度末）"),
                            y=alt.Y(
                                "Net_Income_億円:Q",
                                title="年間当期純利益 (億円)",
                                axis=alt.Axis(
                                    titleColor="#1f77b4", orient="right"
                                ),
                            ),
                            tooltip=[
                                alt.Tooltip(
                                    "Date:T", title="決算期", format="%Y-%m-%d"
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
                    combined_chart = line_fx.interactive()
                    st.warning(
                        "※該当銘柄の年間当期純利益データが取得できませんでした。"
                    )

                st.altair_chart(combined_chart, use_container_width=True)

                st.markdown(
                    '<span style="color:#ff7f0e;">■</span> **ドル円為替（左軸・オレンジ線）** ｜ '
                    '<span style="color:#1f77b4;">■</span> **年間当期純利益（右軸・青色棒グラフ：過去4年分）**',
                    unsafe_allow_html=True,
                )

                with st.expander("詳細な年間財務データを見る"):
                    if not income_df.empty:
                        st.dataframe(income_df[["Net_Income_億円"]])
                    else:
                        st.write("データなし")
            else:
                st.warning("為替データの取得に失敗しました。")
        except Exception as e:
            st.error(f"データの取得・描画中にエラーが発生しました: {e}")