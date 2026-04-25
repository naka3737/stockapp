import streamlit as st

st.set_page_config(page_title="メイン画面", menu_items=None)
st.title("メイン画面")
st.write("分野を選択して下さい。")

# ボタンが押されたら、pagesフォルダ内のファイルへ遷移
# if st.button("自動車株"):
#     st.switch_page("pages/jidousha.py")


if st.button("自動車"):
    st.switch_page("pages/jidousha.py")

if st.button("銀行"):
    st.switch_page("pages/ginkou.py")

if st.button("半導体"):
    st.switch_page("pages/handoutai.py")

if st.button("金属"):
    st.switch_page("pages/kinzoku.py")

if st.button("資源"):
    st.switch_page("pages/shigen.py")

