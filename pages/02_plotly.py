import streamlit as st
import yfinance as yf
import plotly.graph_objs as go
import datetime
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="🌍 글로벌 시가총액 TOP10 주가 변화", layout="wide")
st.title("📈 글로벌 시가총액 TOP10 기업의 최근 1년 주가 변화")

# 시가총액 기준 글로벌 TOP10 (2025년 기준 추정)
tickers = {
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "Saudi Aramco": "2222.SR",  # 사우디 거래소
    "Alphabet (Google)": "GOOGL",
    "Amazon": "AMZN",
    "Nvidia": "NVDA",
    "Berkshire Hathaway": "BRK-B",
    "Meta (Facebook)": "META",
    "TSMC": "TSM",
    "Eli Lilly": "LLY"
}

# 날짜 범위 설정 (최근 1년)
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=365)

# 데이터 로딩 함수 (캐싱)
@st.cache_data
def load_price_data():
    data = {}
    for name, symbol in tickers.items():
        try:
            ticker_data = yf.download(symbol, start=start_date, end=end_date)
            if not ticker_data.empty:
                data[name] = ticker_data['Close']
            else:
                st.warning(f"❗ {name} ({symbol})의 주가 데이터가 없습니다.")
        except Exception as e:
            st.error(f"❌ {name} 데이터 로딩 실패: {e}")
    if not data:
        return None
    return pd.DataFrame(data)

# 데이터 로딩
st.info("📡 주가 데이터를 로딩 중입니다...")
df_prices = load_price_data()

# 데이터 없을 경우 앱 종료
if df_prices is None or df_prices.empty:
    st.error("📉 주가 데이터를 불러오지 못했습니다. 잠시 후 다시 시도해 주세요.")
    st.stop()

# 주가 그래프 시각화
st.subheader("📊 주가 변화 라인 차트 (단위: USD 또는 현지통화)")
fig = go.Figure()

for company in df_prices.columns:
    fig.add_trace(go.Scatter(
        x=df_prices.index,
        y=df_prices[company],
        mode='lines',
        name=company
    ))

fig.update_layout(
    xaxis_title="날짜",
    yaxis_title="주가",
    hovermode="x unified",
    height=600
)

st.plotly_chart(fig, use_container_width=True)
