import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="KBO 누적 관중 시각화", layout="wide")

st.title("⚾ KBO 구단 홈구장 지도 및 누적 관중 시각화")

# KBO 구단 정보
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

# 관중 수 예시 데이터 생성 (실제 CSV나 DB로 교체 가능)
@st.cache_data
def create_dummy_attendance_data():
    dates = pd.date_range("2024-03-23", "2024-09-01")
    data = []
    import random
    for date in dates:
        for team in df_stadiums["팀"]:
            # 예시로 하루 평균 5천~2만 명 생성
            data.append({
                "날짜": date,
                "팀": team,
                "관중수": random.randint(5000, 20000)
            })
    return pd.DataFrame(data)

df_attendance = create_dummy_attendance_data()

# 날짜 선택
selected_date = st.date_input("📅 날짜를 선택하세요", datetime(2024, 7, 1),
                              min_value=datetime(2024, 3, 23),
                              max_value=datetime(2024, 9, 1))

# 누적 관중 계산
df_cumulative = df_attendance[df_attendance["날짜"] <= pd.to_datetime(selected_date)]
df_total_by_team = df_cumulative.groupby("팀")["관중수"].sum().reset_index()

# 구단 정보와 결합
df_total = pd.merge(df_total_by_team, df_stadiums, on="팀")

# 지도 시각화 (pydeck)
st.subheader("📍 홈구장 위치 지도")
deck_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_total,
    get_position='[경도, 위도]',
    get_fill_color='[200, 30, 0, 160]',
    get_radius=50000,
    pickable=True,
)

st.pydeck_chart(pdk.Deck(
    map_style='mapbox://styles/mapbox/light-v9',
    initial_view_state=pdk.ViewState(
        latitude=36.5,
        longitude=127.8,
        zoom=6.2,
        pitch=30,
    ),
    layers=[deck_layer],
    tooltip={"text": "{팀}\n누적 관중: {관중수}명\n구장: {구장}"}
))

# 바 그래프 시각화
st.subheader("📊 누적 관중 수 비교")
fig = px.bar(df_total.sort_values("관중수", ascending=False),
             x="팀", y="관중수", color="팀",
             text="관중수", title=f"{selected_date.strftime('%Y-%m-%d')}까지 누적 관중 수",
             labels={"관중수": "누적 관중 수", "팀": "구단"})

fig.update_traces(texttemplate='%{text:,}', textposition='outside')
fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide', height=500)

st.plotly_chart(fig, use_container_width=True)
