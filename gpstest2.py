import pandas as pd
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from streamlit_geolocation import streamlit_geolocation

st.title("スマホの位置情報リアルタイム追跡テスト")

# --- 自動リフレッシュの設定 ---
# 5000ミリ秒（= 5秒）ごとに自動で画面を再読み込みする
# limit=None にすると無制限に更新を続けます
count = st_autorefresh(interval=5000, limit=None, key="gps_refresh")

st.write(f"自動更新回数: {count} 回目")

# 位置情報コンポーネントの呼び出し
location = streamlit_geolocation()

# 緯度・経度が取得できているか確認
if location.get("latitude") and location.get("longitude"):
  lat = location["latitude"]
  lon = location["longitude"]

  st.success("現在地を追跡中！")
  st.write(f"緯度: {lat}")
  st.write(f"経度: {lon}")

  # 取得した座標をStreamlitの地図に表示
  df = pd.DataFrame({"lat": [lat], "lon": [lon]})
  st.map(df)
else:
  st.warning(
      "位置情報の取得を待っています。スマホのポップアップで「許可」を押してください。"
  )