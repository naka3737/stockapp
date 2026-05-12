import streamlit as st
import pandas as pd
import re
import yfinance as yf

# 1. データの読み込み
# yutai.csv は 'code', '銘柄名', '優待月', '優待内容' の列がある想定です
@st.cache_data
def load_data():
    # 実際のファイルパスに合わせて変更してください
    # 優待月は数値(1-12)として読み込む、あるいは比較時に型を合わせます
    df = pd.read_csv("yutai3.csv", encoding='shift-jis')
    return df

df = load_data()

# セッション状態の初期化（現在選択されている月を保持）
if 'selected_month' not in st.session_state:
    st.session_state.selected_month = None

st.title("月別 株主優待検索")

# 2. 1-12月のボタンを横一列に配置
st.write("### 優待月を選択してください")
cols = st.columns(12)
for i in range(1, 13):
    with cols[i-1]:
        if st.button(f"{i}月", key=f"month_{i}", use_container_width=True):
            st.session_state.selected_month = i

# 3. ボタンが押された（月が選択された）場合の処理
if st.session_state.selected_month:
    # target_month = st.session_state.selected_month

    # month_num = target_month.replace("月", "")
    
    # # 「数字の前に数字がなく、かつ数字の後に数字がない」状態（＝その数字単体）を探す
    # regex_pattern = rf"(?<!\d){month_num}月"

    selected_val = str(st.session_state.selected_month) 
    
    # 2. 「月」という文字を消して数字だけにする（"1月" -> "1", "1" -> "1"）
    month_num = selected_val.replace("月", "")
    
    # 3. 正規表現で「その数字単体」を検索する
    # \D は「数字以外」を意味します。これで11月や12月を除外します。
    target_month = rf"(?<!\d){month_num}月"
    
    #filtered_df = df[df['優待月'].astype(str).str.contains(regex_pattern, na=False, regex=True)]

    


    st.subheader(f"📅 {month_num}月の優待銘柄一覧")

    # データの抽出（"優待月"列が数値の場合を想定）
    #filtered_df = df[df["優待月"] == month]
    #filtered_df = df[df["優待月"].str.contains(target_month, na=False)]
    if target_month:
        #filtered_df = df[df["優待月"].astype(str).str.contains(target_month, na=False)]
        #regex_pattern = f"(?<!\d){str(target_month)}"

        filtered_df = df[df['優待月'].astype(str).str.contains(target_month, na=False, regex=True)]

        #filtered_df = df[df['優待月'].str.contains(str(target_month), na=False)]
        
        if not filtered_df.empty:
            # リスト（セレクトボックス）の作成
            # 表示用に「コード + 銘柄名」のリストを作成
            filtered_df["display_name"] = filtered_df["code"].astype(str) + " " + filtered_df["銘柄名"]
            
            selected_item_name = st.selectbox(
                "詳細を表示する銘柄を選択してください",
                options=filtered_df["display_name"].tolist()
            )

            # 4. 選択された銘柄の詳細を表示
            if selected_item_name:
                # 選択された銘柄のデータを取得
                target_data = filtered_df[filtered_df["display_name"] == selected_item_name].iloc[0]
                
                st.divider()
                st.markdown(f"### 📋 【{target_data['code']}】{target_data['銘柄名']}")
                
                col_info1, col_info2 = st.columns([1, 3])
                with col_info1:
                    # 証券コードを大きく表示
                    st.metric("証券コード", target_data['code'])
                    # その下に優待月を表示
                    st.write("**📅 優待月**")
                    st.write(target_data['優待月'])

                    ticker = yf.Ticker(f"{target_data['code']}.T")
                    price = int(ticker.fast_info.last_price)

                    st.write("**📈 株価**")
                    st.write(str(price) + " 円")

                with col_info2:
                    st.info(f"**優待内容:**\n\n{target_data['優待内容']}")
        else:
            st.warning(f"{month}月の優待データは見つかりませんでした。")