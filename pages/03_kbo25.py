import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
import datetime
import plotly.express as px

st.set_page_config(page_title="🏟️ 2025 KBO 주간 순위 변화", layout="wide")
st.title("📊 2025 KBO 리그 주간 순위 변화 애니메이션")

@st.cache_data(show_spinner=True)
def fetch_weekly_standings():
    start_date = datetime.date(2025, 3, 23)
    end_date = datetime.date.today()
    week_dates = pd.date_range(start=start_date, end=end_date, freq='7D')

    all_data = []
    for date in week_dates:
        date_str = date.strftime("%Y-%m-%d")
        url = f"https://www.koreabaseball.com/Record/TeamRank/TeamRankDaily.aspx?date={date_str}"
        try:
            res = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
            soup = BeautifulSoup(res.text, "html.parser")
            table = soup.find("table", class_="tData")
            if not table:
                continue
            rows = table.select("tbody tr")
            for row in rows:
                cols = row.find_all("td")
                if len(cols) < 2:
                    continue
                team = cols[0].text.strip()
                rank = int(cols[1].text.strip())
                all_data.append({
                    "week": date,
                    "team": team,
                    "rank": rank
                })
        except Exception as e:
            st.warning(f"❌ {date_str} 순위 불러오기 실패: {e}")
    return pd.DataFrame(all_data)

df = fetch_weekly_standings()

if df.empty:
    st.error("❌ 데이터를 불러올 수 없습니다. 사이트 구조가 변경되었을 수 있습니다.")
else:
    fig = px.line(
        df,
        x="team",
        y="rank",
        color="team",
        animation_frame=df["week"].dt.strftime("%Y-%m-%d"),
        range_y=[10.5, 0.5],
        labels={"rank": "순위", "team": "팀"},
        title="🏆 2025 KBO 주간 순위 변화"
    )
    fig.update_yaxes(autorange="reversed")
    fig.update_layout(height=600)
    st.plotly_chart(fig, use_container_width=True)

    week_strs = sorted(df["week"].dt.strftime("%Y-%m-%d").unique())
    selected = st.select_slider("📅 주차를 선택하세요", options=week_strs)
    st.subheader(f"📋 {selected} 기준 순위표")
    selected_df = df[df["week"].dt.strftime("%Y-%m-%d") == selected].sort_values("rank")
    st.table(selected_df.reset_index(drop=True))
