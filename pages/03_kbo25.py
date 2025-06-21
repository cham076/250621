import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import datetime

# 페이지 기본 설정
st.set_page_config(page_title="🏆 2025 KBO 주간 순위 변화", layout="wide")
st.title("📈 2025 KBO 리그 주간별 순위 애니메이션")

# 주간 날짜 리스트 (개막일부터 매주)
start_date = datetime.date(2025, 3, 22)  # KBO 2025 개막일 기준
end_date = datetime.date.today()
weeks = pd.date_range(start=start_date, end=end_date, freq='7D').to_pydatetime().tolist()

# 공식 JSON API로 주간 순위 가져오기
def fetch_rank_snapshot(date: datetime.date):
    url = "https://www.koreabaseball.com/ws/TeamRank/GameRankList.json"
    params = {
        "gameDate": date.strftime("%Y%m%d"),
        "kind": "0"  # 0 = 정규 시즌 순위
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    records = resp.json().get("teamRank", [])
    return [
        {"week": date, "team": rec["teamFullName"], "rank": int(rec["rank"])}
        for rec in records
    ]

# 모든 주차 데이터 수집
all_data = []
for wd in weeks:
    try:
        recs = fetch_rank_snapshot(wd.date())
        if recs:
            all_data.extend(recs)
            st.write(f"✅ {wd.date()} 주차 데이터 로드 성공")
        else:
            st.write(f"⚠️ {wd.date()} 주차 순위 데이터 없음")
    except Exception as e:
        st.warning(f"❌ {wd.date()} 주차 로드 실패: {e}")

# DataFrame 변환 및 검증
df = pd.DataFrame(all_data)
if df.empty:
    st.error("📭 순위 데이터를 하나도 불러오지 못했습니다.")
    st.stop()

# Plotly 애니메이션 라인 차트
fig = px.line(
    df,
    x="team",
    y="rank",
    color="team",
    animation_frame=df['week'].dt.strftime('%Y-%m-%d'),
    range_y=[10.5, 0.5],
    title="2025 KBO 리그 🧢 주간 순위 변화 애니메이션",
    labels={"rank": "순위 (1 = 최고)", "team": "팀"}
)
fig.update_yaxes(autorange="reversed")  # 1위가 위에 표시되도록 반전
fig.update_layout(height=600, legend_title_text='구단명')

st.plotly_chart(fig, use_container_width=True)

# 주차 슬라이더 및 테이블 UI
week_strs = sorted(df['week'].dt.strftime('%Y-%m-%d').unique())
selected_week = st.select_slider("🔢 특정 주차 선택", options=week_strs)
sub = df[df['week'].dt.strftime('%Y-%m-%d') == selected_week].sort_values("rank").reset_index(drop=True)
st.write(f"### 📅 {selected_week} 주차 순위표")
st.table(sub)
