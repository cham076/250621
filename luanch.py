import streamlit as st
import requests
import datetime
import random

API_KEY = "YOUR_NEIS_API_KEY"  # 발급받은 키로 교체하세요.
SCHOOL_CODE = "B000011986"     # 충암고등학교 NEIS 학교 코드
ORG_CODE = "J10"               # 서울특별시 교육청 코드

st.set_page_config(page_title="🍽️ 충암고 급식 앱", layout="centered")

st.markdown("""
<h1 style="text-align:center;color:#FF6347;">🍱 충암고등학교 급식 보기</h1>
<p style="text-align:center;font-size:18px;">날짜를 선택해서 오늘의 급식을 확인해보세요!</p>
<hr>
""", unsafe_allow_html=True)

selected_date = st.date_input("📅 급식을 볼 날짜를 선택하세요",
                              datetime.date.today(),
                              min_value=datetime.date(2024,1,1),
                              max_value=datetime.date.today())

yyyymm = selected_date.strftime("%Y%m")
yyyymmdd = selected_date.strftime("%Y%m%d")

params = {
    "KEY": 45792ab9f62d44bdb406d69d79e08c37,
    "Type": "json",
    "ATPT_OFCDC_SC_CODE": ORG_CODE,
    "SD_SCHUL_CODE": SCHOOL_CODE,
    "MLSV_YMD": yyyymmdd
}

st.markdown(f"### 📌 {selected_date.strftime('%Y년 %m월 %d일')} 급식 메뉴")

resp = requests.get("https://open.neis.go.kr/hub/mealServiceDietInfo", params=params)
data = resp.json()

if "mealServiceDietInfo" not in data:
    st.warning("해당 날짜의 급식 정보가 없습니다.")
else:
    info = data["mealServiceDietInfo"][1]["row"][0]
    dishes = info["DDISH_NM"].split("<br/>")
    cal = info.get("CAL_INFO", "정보 없음")
    nutrient = info.get("NTR_INFO", "영양 정보 없음")
    
    emoji_review = random.choice([
        "😋 오늘도 든든! 최고야~",
        "👍 맛있는 한 끼!",
        "😊 건강하게 먹어요!",
        "🙌 균형 잡힌 식사입니다!"
    ])
    
    st.markdown("---")
    for item in dishes:
        st.markdown(f"- 🍽️ **{item}**")
    st.markdown(f"\n**🔥 칼로리**: {cal}")
    st.markdown(f"**🧠 영양**: {nutrient}")
    st.markdown(f"\n### 💬 한줄 평\n> {emoji_review}")
    st.markdown("---")
    st.markdown('<p style="text-align:center;font-size:14px;">Made with ❤️ by SchoolMealBot</p>',
                unsafe_allow_html=True)
