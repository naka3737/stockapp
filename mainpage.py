import streamlit as st

st.title("メイン画面")
st.write("分野を選択して下さい。")
シリタ
# ボタンが押されたら、pagesフォルダ内のファイルへ遷移
# if st.button("自動車株"):
#     st.switch_page("pages/jidousha.py")


if st.button("自働車"):
    st.switch_page("pages/jidousha.py")

if st.button("金属"):
    st.switch_page("pages/kinzoku.py")

if st.button("資源"):
    st.switch_page("pages/shigen.py")