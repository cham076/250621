import streamlit as st
import pandas as pd
import pydeck as pdk
import plotly.express as px
from datetime import datetime
import random

# 페이지 설정
st.set_page_config(page_title="KBO 누적 관중 시각화", layout="wide")
st.title("⚾ KBO 구단 홈구장 지도 및 누적 관중 시각화")

# 팀 정보
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

# 로고 URL
team_logos = {
    "LG 트윈스": "https://upload.wikimedia.org/wikipedia/en/2/2f/LG_Twins.png",
    "두산 베어스": "https://upload.wikimedia.org/wikipedia/en/2/24/Doosan_Bears.png",
    "SSG 랜더스": "https://upload.wikimedia.org/wikipedia/en/f/fd/SSG_Landers.png",
    "KT 위즈": "https://upload.wikimedia.org/wikipedia/en/3/3c/KT_Wiz.png",
    "NC 다이노스": "https://upload.wikimedia.org/wikipedia/en/e/e1/NC_Dinos.png",
    "KIA 타이거즈": "https://upload.wikimedia.org/wikipedia/en/8/8e/Kia_Tigers.png",
    "삼성 라이온즈": "https://upload.wikimedia.org/wikipedia/en/7/71/Samsung_Lions.png",
    "한화 이글스": "https://upload.wikimedia.org/wikipedia/en/f/fd/Hanwha_Eagles.png",
    "롯데 자이언츠": "https://upload.wikimedia.org/wikipedia/en/0/04/Lotte_Giants.png",
    "키움 히어로즈": "https://upload.wikimedia.org/wikipedia/en/e/e3/Kiwoom_Heroes.png"
}

# 가상 관중 데이터 생성
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

# 날짜 범위 슬라이더
min_date = df_attendance["날짜"].min().date()
max_date = df_attendance["날짜"].max().date()

date_range = st.slider(
    "📆 날짜 범위 선택",
    min_value=min_date,
    max_value=max_date,
    value=(min_date, max_date),
    format="YYYY-MM-DD"
)

start_date = pd.to_datetime(date_range[0])
end_date = pd.to_datetime(date_range[1])

# 누적 관중 계산
df_filtered = df_attendance[(df_attendance["날짜"] >= start_date) & (df_attendance["날짜"] <= end_date)]
df_total_by_team = df_filtered.groupby("팀")["관중수"].sum().reset_index()
df_total = pd.merge(df_total_by_team, df_stadiums, on="팀")

# 색 농도용 알파값 계산
max_audience = df_total["관중수"].max()
df_total["alpha"] = (df_total["관중수"] / max_audience * 255).clip(60, 255).astype(int)

# 로고 정보 추가
df_total["icon_url"] = df_total["팀"].map(team_logos)
df_total["icon_data"] = df_total.apply(lambda row: {
    "url": row["icon_url"],
    "width": 128,
    "height": 128,
    "anchorY": 128
}, axis=1)

# 지도 시각화
st.subheader("📍 홈구장 위치 지도 (API 없이 지도 배경 표시)")

scatter_layer = pdk.Layer(
    "ScatterplotLayer",
    data=df_total,
    get_position='[경도, 위도]',
    get_fill_color='[255, 80, 80, alpha]',
    get_radius=10000,
    pickable=True
)

icon_layer = pdk.Layer(
    "IconLayer",
    data=df_total,
    get_icon="icon_data",
    get_size=4,
    size_scale=10,
    get_position='[경도, 위도]',
    pickable=False
)

view_state = pdk.ViewState(
    latitude=36.3,
    longitude=127.8,
    zoom=6.3,
    pitch=30
)

st.pydeck_chart(pdk.Deck(
    map_style=None,  # ✅ API 없이 지도 배경 표시
    initial_view_state=view_state,
    layers=[scatter_layer, icon_layer],
    tooltip={"text": "{팀}\n구장: {구장}\n누적 관중: {관중수}명"}
))

# 누적 관중 바 차트
st.subheader("📊 누적 관중 수 (선택한 날짜 범위)")
fig = px.bar(
    df_total.sort_values("관중수", ascending=False),
    x="팀", y="관중수", color="팀",
    text="관중수",
    labels={"관중수": "누적 관중 수", "팀": "구단"},
    title=f"{start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')} 누적 관중 수"
)
fig.update_traces(texttemplate='%{text:,}', textposition='outside')
fig.update_layout(height=500)
st.plotly_chart(fig, use_container_width=True)

# 팀별 관중 변화 추이
st.subheader("📈 팀별 관중 변화 추이")
df_line = df_attendance[(df_attendance["날짜"] >= start_date) & (df_attendance["날짜"] <= end_date)]
df_line = df_line.groupby(["날짜", "팀"])["관중수"].sum().reset_index()

fig_line = px.line(
    df_line, x="날짜", y="관중수", color="팀",
    title="날짜별 구단별 관중 수 추이",
    labels={"관중수": "일일 관중 수"}
)
fig_line.update_layout(height=500)
st.plotly_chart(fig_line, use_container_width=True)

# 팀별 상세 분석
st.subheader("🔍 팀별 상세 분석")
selected_teams = st.multiselect("자세히 보고 싶은 팀을 선택하세요:", df_stadiums["팀"].unique())

if selected_teams:
    for team in selected_teams:
        st.markdown(f"### 📌 {team}")
        team_data = df_attendance[(df_attendance["팀"] == team) &
                                  (df_attendance["날짜"] >= start_date) &
                                  (df_attendance["날짜"] <= end_date)]
        total = team_data["관중수"].sum()
        avg = int(team_data["관중수"].mean())
        st.write(f"**총 누적 관중수**: {total:,}명")
        st.write(f"**평균 관중수**: {avg:,}명")

        fig_team = px.line(team_data, x="날짜", y="관중수",
                           title=f"{team} 일일 관중 변화", labels={"관중수": "관중수"})
        fig_team.update_layout(height=300)
        st.plotly_chart(fig_team, use_container_width=True)
