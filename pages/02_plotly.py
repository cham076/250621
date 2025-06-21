import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import datetime
import pandas as pd

# 🌍 페이지 설정
st.set_page_config(page_title="🌍 글로벌 TOP10 주가 변화", layout="wide")
st.title("📈 글로벌 시가총액 TOP10 기업의 최근 1년 주가 변화")

# 🔎 티커 목록 (2025 기준 추정)
tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    "Eli Lilly": "LLY",
    # "Saudi Aramco": "2222.SR"  # 제외: 사우디 증시 데이터 수집 오류 가능성
}

# 📅 날짜 설정
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

# 📥 데이터 수집 함수
@st.cache_data(show_spinner=True)
def load_data():
    collected = {}
    for name, symbol in tickers.items():
        try:
            df = yf.download(symbol, start=start_date, end=end_date)
            if not df.empty:
                collected[name] = df['Adj Close']
        except Exception as e:
            st.warning(f"{name} ({symbol}) 데이터 수집 실패: {e}")
    return pd.DataFrame(collected)

data = load_data()

# 🚨 데이터 없을 경우 처리
if data.empty:
    st.error("📭 데이터를 불러오지 못했습니다. 나중에 다시 시도해 주세요.")
else:
    # 📈 Plotly 그래프 그리기
    fig = go.Figure()
    for company in data.columns:
        fig.add_trace(go.Scatter(
            x=data.index, y=data[company],
            mode='lines', name=company
        ))

    fig.update_layout(
        title="📊 최근 1년간 글로벌 시가총액 TOP10 기업 주가 변화",
        xaxis_title="날짜",
        yaxis_title="조정 종가 (USD)",
        template="plotly_white",
        hovermode="x unified",
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)
