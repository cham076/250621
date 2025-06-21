import streamlit as st
import requests
from bs4 import BeautifulSoup
import datetime
import random

st.set_page_config(page_title="🍱 충암고 급식앱", layout="centered")

st.markdown("""
<h1 style="text-align:center;color:#FF4500;">🌟 충암고등학교 급식 조회</h1>
<p style="text-align:center;font-size:18px;">날짜를 선택해 오늘의 중식 메뉴를 확인하세요!</p>
<hr>
""", unsafe_allow_html=True)

# 날짜 입력
selected = st.date_input("📅 날짜 선택", datetime.date.today(), min_value=datetime.date(2024,1,1), max_value=datetime.date.today())

yyyymm = selected.strftime("%Y%m")
yyyymmdd = selected.day

# 스크래핑용 URL (예: june 2025)
url = f"https://school.koreacharts.com/school/meals/B000011986/{yyyymm}.html"
resp = requests.get(url)
soup = BeautifulSoup(resp.text, "html.parser")

# 메뉴 추출
rows = soup.select("table tr")
menu = None
for r in rows:
    cols = r.find_all("td")
    if len(cols)>=3:
        day = cols[0].get_text(strip=True)
        if int(day) == yyyymmdd:
            text = cols[2].get_text(separator="\n", strip=True)
            menu = text
            break

# 결과 표시
st.markdown(f"### 📌 {selected.strftime('%Y년 %m월 %d일')} 중식 메뉴")
if not menu:
    st.warning("해당 날짜의 급식 정보가 없습니다.")
else:
    lines = menu.split("\n")
    dishes = [l for l in lines if l and not l.startswith("[")]
    cal = "-"
    nutri = "-"
    # 칼로리/영양 정보는 다른 사이트 필요하므로 생략

    emoji = random.choice(["😋 든든해요!", "👍 맛있었어요!", "😊 건강하게!", "💚 영양 만점!"])
    st.markdown("---")
    for d in dishes:
        st.markdown(f"- 🍲 **{d}**")
    st.markdown(f"\n### 💬 한줄 평: *{emoji}*")
    st.markdown("---")
    st.markdown('<p style="text-align:center;font-size:14px;">Made with ❤️ by SchoolMealBot</p>', unsafe_allow_html=True)
