import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
import datetime

st.set_page_config(page_title="📈 KBO 2025 주간 순위 변화", layout="wide")
st.title("2025년 KBO 10개 구단 주간 순위 변화")

# 예시 주간 URL들: 실제 정보를 가지는 URL로 교체 필요
example_weeks = {
    "2025-04-06": "https://mykbostats.com/week/2025-04-06/standings",
    "2025-05-04": "https://mykbostats.com/week/2025-05-04/standings",
    "2025-06-15": "https://mykbostats.com/week/2025-06-15/standings",
}

def fetch_week_data(date_str, url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text, "html.parser")
    table = soup.select_one("table")  # 실제 HTML 구조에 맞게 수정 필요
    rows = table.find_all("tr")[1:]
    data = []
    for r in rows:
        cols = r.find_all("td")
        team = cols[1].get_text(strip=True)
        rank = int(cols[0].get_text(strip=True))
        data.append({"week": pd.to_datetime(date_str), "team": team, "rank": rank})
    return data

all_data = []
for date_str, url in example_weeks.items():
    try:
        all_data += fetch_week_data(date_str, url)
    except Exception:
        st.warning(f"{date_str} 데이터 가져오기 실패: {url}")

df = pd.DataFrame(all_data)

if df.empty:
    st.error("순위 데이터를 가져오지 못했습니다.")
else:
    fig = px.line(df, x="week", y="rank", color="team",
                  markers=True, title="🏆 주간 순위 변화 (랭킹이 낮을수록 상위)",
                  labels={"rank": "순위", "week": "주간"})
    fig.update_yaxes(autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)
