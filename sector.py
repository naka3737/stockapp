import streamlit as st
import yfinance as yf
import pandas as pd


def csector(sec):

    match sec:
        case "Energy":
            sname = "エネルギー"
        case "Materials":
            sname = "素材"
        case "Industrials":
            sname = "資本材・サービス"
        case "Consumer Discretionary":
            sname = "一般消費財"
        case "Consumer Staples":
            sname = "生活必需品"
        case "Health Care":
            sname = "ヘルスケア"
        case "Financials":
            sname = "金融"
        case "Information Technology":
            sname = "情報技術"
        case "Communication Services":
            sname = "コミュニケーションサービス"
        case "Utilities":
            sname = "公共事業"
        case "Real Estate":
            sname = "不動産"
        case _:
            # 💡 万が一、上記の11個以外の文字が来たら、そのままの英語を返す安全対策
            sname = sec
            
    return sname;

