import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(page_title="🏆 2025 KBO 주간 순위 변화", layout="wide")
st.title("📈 2025 KBO 리그 주간별 순위 변화")

# 📅 주간 날짜 리스트 생성 (개막 주 ~ 현재)
start_date = datetime.date(2025, 3, 22)  # 2025 KBO 개막일
end_date = datetime.date.today()
weeks = pd.date_range(start=start_date, end=end_date, freq='7D').to_pydatetime().tolist()

# ⚙️ 주간 순위 스크래핑 함수
def fetch_standings(date):
    url = f"https://mykbostats.com/week/{date.strftime('%Y-%m-%d')}/standings"  # 예시 URL
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.select_one("table")  # 실제 구조에 맞게 조정 필요
    data = []
    for row in table.select("tr")[1:]:
        cols = row.find_all("td")
        rank = int(cols[0].text.strip())
        team = cols[1].text.strip()
        data.append({"week": date, "team": team, "rank": rank})
    return data

# 🔄 데이터 수집
all_data = []
for wd in weeks:
    try:
        all_data += fetch_standings(wd)
    except Exception as e:
        st.warning(f"{wd.date()} 순위 스크래핑 실패: {e}")

df = pd.DataFrame(all_data)
if df.empty:
    st.error("⚠️ 순위 데이터를 가져오지 못했습니다.")
else:
    st.success("✅ 주간 순위 데이터 로드 완료!")

    # 🎨 Plotly 애니메이션 그래프
    fig = px.line(
        df, x="team", y="rank", color="team",
        animation_frame=df['week'].dt.strftime('%Y-%m-%d'),
        range_y=[10.5, 0.5],  # 순위가 1~10
        title="2025 KBO 리그 주간 순위 변화 📊",
        labels={"rank": "순위 (1 = 최고)", "team": "팀"}
    )
    fig.update_yaxes(autorange="reversed")  # 1위가 위에 표시
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    # 🔧 주차 슬라이더 표시
    week_strs = sorted(df['week'].dt.strftime('%Y-%m-%d').unique())
    selected = st.select_slider("🔢 주차 선택", options=week_strs)
    sub = df[df['week'].dt.strftime('%Y-%m-%d') == selected]
    st.write(f"### 📅 {selected} 주차 순위")
    st.table(sub.sort_values("rank").reset_index(drop=True))
