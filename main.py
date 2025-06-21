import streamlit as st
import random

# MBTI별 직업 추천 딕셔너리
career_recommendations = {
    "ISTJ": ["🧑‍⚖️ 판사", "💼 회계사", "🏛️ 행정 공무원"],
    "ISFJ": ["👩‍⚕️ 간호사", "👨‍🏫 교사", "🧸 사회복지사"],
    "INFJ": ["🧘‍♂️ 상담가", "📖 작가", "🧠 심리학자"],
    "INTJ": ["💡 전략가", "🔬 과학자", "📊 데이터 분석가"],
    "ISTP": ["🛠️ 엔지니어", "🚔 경찰관", "🧰 정비사"],
    "ISFP": ["🎨 아티스트", "👗 패션 디자이너", "🎭 무대 디자이너"],
    "INFP": ["📚 작가", "🎼 작곡가", "🌍 환경운동가"],
    "INTP": ["🤖 개발자", "🔭 물리학자", "🧮 수학자"],
    "ESTP": ["🚒 소방관", "📣 마케터", "🎬 배우"],
    "ESFP": ["🎤 가수", "📺 방송인", "🎪 퍼포머"],
    "ENFP": ["🧳 여행가이드", "📚 작가", "🗣️ 연설가"],
    "ENTP": ["📈 기업가", "💬 토론가", "🧪 발명가"],
    "ESTJ": ["🏦 은행원", "🧱 건축가", "🧾 관리자"],
    "ESFJ": ["👩‍🍳 요리사", "🎓 교사", "🧑‍⚕️ 의료 코디네이터"],
    "ENFJ": ["🗽 사회운동가", "🎙️ MC", "👨‍🏫 교육자"],
    "ENTJ": ["📊 CEO", "🏛️ 정치가", "🧭 경영 컨설턴트"]
}

# 앱 타이틀 및 꾸미기
st.set_page_config(page_title="✨ MBTI 직업 추천기 ✨", layout="centered")
st.markdown("""
    <h1 style='text-align: center; color: #FF69B4;'>🌟 MBTI 기반 진로 추천 🌈</h1>
    <p style='text-align: center; font-size: 20px;'>당신의 MBTI는 무엇인가요? 알맞은 직업을 추천해드릴게요! 🎯</p>
    <hr>
""", unsafe_allow_html=True)

# MBTI 선택
mbti_list = list(career_recommendations.keys())
selected_mbti = st.selectbox("📌 MBTI를 선택하세요:", mbti_list, index=0)

if selected_mbti:
    st.markdown(f"### 🧬 당신의 MBTI: **{selected_mbti}**")
    jobs = career_recommendations[selected_mbti]
    recommended = random.choice(jobs)
    st.markdown(f"## 🎉 추천 직업: {recommended}")
    st.markdown("""
    <p style='font-size: 18px;'>🌟 다른 직업을 보고 싶다면 다시 선택해보세요!</p>
    <hr>
    <p style='text-align: center; font-size: 16px;'>Made with ❤️ by CareerBot</p>
    """, unsafe_allow_html=True)

# 꾸미기용 배경 이미지 및 스타일 추가 가능 (선택적으로 HTML/CSS 추가 가능)
