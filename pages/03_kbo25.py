import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from datetime import datetime
import random

# 페이지 설정
st.set_page_config(page_title="KBO 누적 관중 시각화", layout="wide")
st.title("⚾ KBO 구단 홈구장 지도 및 누적 관중 시각화")

# 구단 위치 및 구장 정보
teams = [
    {"팀": "LG 트윈스", "위도": 37.5125, "경도": 127.0728, "구장": "잠실"},
    {"팀": "두산 베어스", "위도": 37.5125, "경도": 127.0728, "구장": "잠실"},
    {"팀": "SSG 랜더스", "위도": 37.4350, "경도": 126.6930, "구장": "인천"},
    {"팀": "KT 위즈", "위도": 37.3213, "경도": 127.0109, "구장": "수원"},
    {"팀": "NC 다이노스", "위도": 35.2225, "경도": 128.5805, "구장": "창원"},
    {"팀": "KIA 타이거즈", "위도": 35.1682, "경도": 126.8886, "구장": "광주"},
    {"팀": "삼성 라이온즈", "위도": 35.8417, "경도": 128.6811, "구장": "대구"},
    {"팀": "한화 이글스", "위도": 36.3173, "경도": 127.4280, "구장": "대전"},
    {"팀": "롯데 자이언츠", "위도": 35.1944, "경도": 129.0592, "구장": "부산"},
    {"팀": "키움 히어로즈", "위도": 37.5663, "경도": 126.8972, "구장": "고척"}
]
df_stadiums = pd.DataFrame(teams)

# 예시용 관중수 데이터 생성
@st.cache_data
def create_dummy_attendance_data():
    start = datetime(2024, 3, 23)
    end = datetime.today()
    dates = pd.date_range(start, end)
    data = []
    for date in dates:
        for team in df_stadiums["팀"]:
            data.append({
                "날짜": date,
                "팀": team,
                "관중수": random.randint(5000, 20000)
            })
    return pd.DataFrame(data)

df_attendance = create_dummy_attendance_data()

# 날짜 범위 슬라이더용 date 타입으로 변환
min_date = df_attendance["날짜"].min().date()
max_date = df_attendance["날짜"].max().date()

# 슬라이더 UI
date_range = st.slider(
    "📆 날짜 범위 선택",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

# 슬라이더 결과값을 datetime으로 변환
start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# 필터링된 누적 관중
df_filtered = df_attendance[(df_attendance["날짜"] >= start_date) & (df_attendance["날짜"] <= end_date)]
df_total_by_team = df_filtered.groupby("팀")["관중수"].sum().reset_index()
df_total = pd.merge(df_total_by_team, df_stadiums, on="팀")

# 지도 시각화
st.subheader("📍 홈구장 위치 지도 (누적 관중 포함)")
deck_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_total,
    get_position='[경도, 위도]',
    get_fill_color='[255, 100, 100, 160]',
    get_radius='관중수 / 10',
    pickable=True
)

view_state = pdk.ViewState(
    latitude=36.3,
    longitude=127.8,
    zoom=6.3,
    pitch=30
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=view_state,
    layers=[deck_layer],
    tooltip={"text": "{팀}\n구장: {구장}\n누적 관중: {관중수}명"}
))

# 그래프 시각화
st.subheader("📊 누적 관중 수 (선택한 날짜 범위)")
fig = px.bar(
    df_total.sort_values("관중수", ascending=False),
    x="팀", y="관중수", color="팀",
    text="관중수",
    labels={"관중수": "누적 관중 수", "팀": "구단"},
    title=f"{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')} 누적 관중 수"
)

fig.update_traces(texttemplate='%{text:,}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', height=500)

st.plotly_chart(fig, use_container_width=True)
