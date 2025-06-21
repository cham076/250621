import streamlit as st
import pandas as pd
import pydeck as pdk

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_csv("growup.csv", encoding="cp949")
    return df

df = load_data()

# 좌표 데이터 불러오기 (서울 시군구 중심 위도/경도, 필요시 전국으로 확장 가능)
# 여기선 서울 시군구 예시 (수동 설정 또는 geopy로 자동화 가능)
locations = {
    "종로구": [37.573050, 126.979189],
    "중구": [37.563750, 126.997559],
    "용산구": [37.532600, 126.990100],
    "성동구": [37.563400, 127.036100],
    "광진구": [37.538400, 127.082800],
    "동대문구": [37.5744, 127.0396],
    "중랑구": [37.6063, 127.0927],
    "성북구": [37.5894, 127.0167],
    "강북구": [37.6396, 127.0253],
    "도봉구": [37.6688, 127.0472],
    "노원구": [37.6543, 127.0568],
    "은평구": [37.6176, 126.9227],
    "서대문구": [37.5792, 126.9368],
    "마포구": [37.5663, 126.9013],
    "양천구": [37.5172, 126.8664],
    "강서구": [37.5509, 126.8495],
    "구로구": [37.4955, 126.8877],
    "금천구": [37.4601, 126.9007],
    "영등포구": [37.5264, 126.8962],
    "동작구": [37.5124, 126.9395],
    "관악구": [37.4784, 126.9516],
    "서초구": [37.4836, 127.0326],
    "강남구": [37.5172, 127.0473],
    "송파구": [37.5145, 127.1059],
    "강동구": [37.5302, 127.1238]
}

# 사용자 선택: 연도
years = df["연도"].unique()
selected_year = st.selectbox("연도 선택", sorted(years, reverse=True))
df_year = df[df["연도"] == selected_year].copy()

# 좌표 추가
df_year["위도"] = df_year["시군구"].map(lambda x: locations.get(x, [None, None])[0])
df_year["경도"] = df_year["시군구"].map(lambda x: locations.get(x, [None, None])[1])
df_year = df_year.dropna(subset=["위도", "경도"])

# 알파값(진학률 시각화용)
max_rate = df_year["진학률"].max()
df_year["alpha"] = (df_year["진학률"] / max_rate * 255).clip(50, 255).astype(int)

# 지도 시각화
st.subheader("🗺️ 시군구별 대학 진학률 지도")

layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_year,
    get_position='[경도, 위도]',
    get_fill_color='[30, 144, 255, alpha]',  # 파란색 계열
    get_radius=8000,
    pickable=True
)

view_state = pdk.ViewState(
    latitude=37.55,
    longitude=126.98,
    zoom=10,
    pitch=20
)

st.pydeck_chart(pdk.Deck(
    map_style=None,  # ✅ API 없이 지도 사용
    initial_view_state=view_state,
    layers=[layer],
    tooltip={"text": "{시군구}\n진학률: {진학률}%"}
))
