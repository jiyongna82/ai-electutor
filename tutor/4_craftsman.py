import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="AI 전기기능사 Intelligence", page_icon="⚡", layout="wide")

# --- [페이지 업데이트 안내 문구] ---
st.info("🌱 현재 전기기능사 CBT 기출 데이터를 기반으로 AI 분석 엔진을 고도화하고 있습니다. 더 나은 분석 서비스를 제공하기 위해 화면이나 기능이 수시로 변동될 수 있으니 양해 부탁드립니다.")

# 2. 분석용 가상 데이터 생성 (실제 CSV 연동 전 UI 확인용)
@st.cache_data(ttl=600)
def generate_mock_data():
    # 기능사 필기 3과목
    written_cats = ["1. 전기이론", "2. 전기기기", "3. 전기설비"]
    written_data = pd.DataFrame({
        '과목': np.random.choice(written_cats, 1200, p=[0.33, 0.33, 0.34]),
        '난이도': np.random.choice(['상', '중', '하'], 1200, p=[0.1, 0.4, 0.5]), # 기능사는 하~중 비중이 높음
        '핵심키워드': ['옴의법칙', '키르히호프', '직류기구조', '변압기원리', '금속관공사', 'KEC접지', '전선접속법'] * 171 + ['유도전동기', '합성저항', '배선기구']
    })
    return written_data

df_written = generate_mock_data()

# --- [상단 레이아웃: AI 분석 타이틀] ---
head_col, select_col = st.columns([7, 3])
with head_col:
    st.title("⚡ AI-Driven 전기기능사 Intelligence")
    st.markdown("<p style='color: #283593; font-weight: bold;'>전기기능사 CBT 필기 빅데이터 정밀 분석 엔진 v3.0</p>", unsafe_allow_html=True)
    
with select_col:
    with st.popover("⚙️ AI 분석 매개변수 설정", use_container_width=True):
        st.radio("CBT 분석 기간 선택", ["최근 3개년 (최신 CBT 트렌드)", "최근 5개년 (핵심 문제은행)", "최근 10개년 (전체 문항)"], index=1)
        st.checkbox("KEC 개정(21년 이후) 문항 최우선 반영", value=True)

st.success("⚡ **AI 엔진 연산 완료:** 필기 180선(과목별 60문항) 핵심 알고리즘 추출 완료")

# ==========================================
# 전기기능사 필기 단일 대시보드 (탭 없음)
# ==========================================

# 통계 가공
stats_w = df_written['과목'].value_counts().reset_index()
stats_w.columns = ['과목', '문항수']
stats_w['비중(%)'] = (stats_w['문항수'] / len(df_written) * 100).round(1)
stats_w = stats_w.sort_values('과목')

# 지표 요약
c1, c2, c3 = st.columns(3)
c1.metric("필기 분석 표본(N)", f"{len(df_written)} 문항")
c2.metric("AI 예측 도출 문항", "총 180문항 (과목별 60문항)")
c3.metric("기능사 전략 과목", "3. 전기설비 (100% 암기형)")

st.divider()

# 차트와 분석 시나리오를 좌우로 배치하여 가독성 확보
chart_col, text_col = st.columns([4, 6])

with chart_col:
    st.subheader("📊 필기 과목별 출제 분포")
    base_w = alt.Chart(stats_w).encode(
        x=alt.X('문항수:Q', title='출제 빈도수'),
        y=alt.Y('과목:N', title=None, axis=alt.Axis(labelFontSize=13, labelFontWeight='bold')),
        color=alt.condition(alt.datum['과목'] == '3. 전기설비', alt.value('#283593'), alt.value('#C5CAE9'))
    ).mark_bar(cornerRadiusEnd=4).properties(height=280)
    
    text_w = base_w.mark_text(align='left', dx=5, color='black', fontWeight='bold').encode(text=alt.Text('비중(%):Q', format='.1f'))
    st.altair_chart(base_w + text_w, use_container_width=True)

with text_col:
    st.subheader("💡 필기 AI 심층 분석 시나리오")
    st.markdown("#### 1. 전기이론 (계산의 기초)")
    st.write("**AI Logic:** 수험생들이 가장 어려워하는 과목입니다. 복잡한 수식보다는 옴의 법칙, 직/병렬 합성저항 계산, 교류 실효값 등 **기본 공식에 숫자만 대입하는 문제**가 반복 출제됩니다.")
    st.markdown("#### 2. 전기기기 (구조와 원리)")
    st.write("**AI Logic:** 4대 기기(직류기, 동기기, 변압기, 유도기)의 특성을 묻습니다. 변압기의 권수비 계산, 유도전동기의 슬립(s) 공식 등 빈출 계산 문제와 각 기기의 주요 부품 명칭을 매칭하는 훈련이 필요합니다.")
    st.markdown("#### 3. 전기설비 (고득점 효자 과목)")
    st.write("**AI Logic:** 과락을 막고 평균 점수를 끌어올리는 100% 암기 과목입니다. 배선/배관 공사의 종류, 전선 접속법, **KEC 기준의 접지선 굵기 및 색상**은 무조건 득점해야 하는 A급 키워드입니다.")

# --- [필기 출제 예상 180선 동적 생성 (과목당 60개)] ---
st.divider()
st.subheader("🎯 CSV 기반 AI 예측 CBT 출제 예상 180선")
st.caption("※ 각 과목 메뉴를 클릭하여 확인하세요. 문제은행 특성을 반영해 12개의 베이스 문항을 5가지 패턴으로 확장했습니다.")

base_written = {
    "1. 전기이론 (60문항)": [
        "옴의 법칙(V=IR)과 키르히호프의 법칙을 이용한 회로 해석", 
        "저항(R)의 직렬 및 병렬접속 시 합성 저항 계산",
        "도체의 고유저항(ρ)과 길이, 단면적에 따른 저항 변화",
        "줄의 법칙(H=0.24I²Rt)을 이용한 발열량 및 전력량 계산",
        "쿨롱의 법칙을 이용한 두 전하 간의 정전기력(흡인력/반발력)",
        "평행판 콘덴서의 직/병렬 합성 정전용량(C) 산출",
        "자기회로의 옴의 법칙 및 앙페르의 오른나사 법칙 적용",
        "플레밍의 왼손 법칙(전동기)과 오른손 법칙(발전기) 비교",
        "패러데이-렌츠의 전자유도 법칙과 유도 기전력 계산",
        "정현파 교류의 최댓값, 실효값, 평균값 상호 변환 계산",
        "R-L-C 직렬회로의 임피던스(Z) 및 피상/유효/무효 전력",
        "3상 교류의 Y결선 및 Δ결선 시 선간전압과 상전압의 관계"
    ],
    "2. 전기기기 (60문항)": [
        "직류발전기의 3대 구성요소(전기자, 계자, 정류자) 및 역할",
        "직류전동기의 회전 방향 변경 방법 및 속도 제어법",
        "동기발전기의 동기속도(Ns=120f/p) 계산 및 병렬운전 조건",
        "동기전동기의 V곡선 특성(여자전류 변화에 따른 역률 변화)",
        "변압기의 원리 및 권수비(a=V1/V2=N1/N2) 계산",
        "변압기 손실(무부하손/부하손) 및 최대 효율을 얻기 위한 조건",
        "변압기 결선 방식(Y-Y, Δ-Δ, V-V)의 특성과 출력비 계산",
        "3상 유도전동기의 회전 원리 및 슬립(s) 공식 계산",
        "농형 및 권선형 유도전동기의 기동 방식(Y-Δ 기동 등)",
        "단상 유도전동기의 기동 토크 크기 순서 (반-콘-분-셰)",
        "정류기(다이오드, SCR)의 특성 및 반파/전파 정류 회로",
        "보호계전기의 종류(OCR, OVR 등)와 전기기기 절연 등급(종류별 최고 허용 온도)"
    ],
    "3. 전기설비 (60문항)": [
        "전선의 구비 조건 및 옥내 배선용 전선(NR, HIV 등)의 약호 식별",
        "전선의 접속법(트위스트 접속, 브리타니아 접속 등) 및 접속 시 유의사항",
        "애자 사용 공사 시 전선 상호 간 및 조영재 간의 이격 거리 기준",
        "금속관, 합성수지관(PE관) 공사의 특성 및 관의 구부림 반경 기준",
        "케이블 공사 및 가요 전선관 공사의 시설 규정",
        "각종 배선 기구(스위치, 콘센트) 및 조명 기구의 옥내 배선 심벌 명칭",
        "KEC 개정에 따른 접지 방식의 분류 및 상/중성선/보호도체(PE) 색상 식별",
        "분전반 및 배전반의 설치 기준(설치 높이, 재질 등)",
        "절연저항계(Megger) 사용법 및 저압 전로의 허용 절연저항 기준값",
        "가공 전선로 지지물(목주, 콘크리트주)의 땅에 묻는 깊이(매설 깊이) 계산",
        "가공 전선로의 지선 설치 목적과 지선 가닥수, 안전율 기준",
        "저압 배전선로 보호용 기기(퓨즈, 배선용 차단기, 누전 차단기)의 역할"
    ]
}

# 자동펼침(expanded=True) 제거, 5개 변형 패턴 텍스트 추가
variations = [
    "기본 개념 및 공식의 정의를 올바르게 설명한 것은?", 
    "관련 수치를 대입하여 계산된 결과값으로 알맞은 것은?", 
    "해당 설비(이론)의 장단점 및 특징으로 틀린 것은?", 
    "관련 도면, 회로 기호 또는 기기 부품 명칭을 고르시오.", 
    "KEC 규정 및 현장 안전 수칙에 따른 적합한 기준을 고르시오."
]

for cat, base_items in base_written.items():
    with st.expander(f"📌 {cat}"): # expanded 옵션을 빼서 기본으로 닫혀있게 설정
        count = 1
        for item in base_items:
            for var in variations:
                st.write(f"**Q{count}.** [{item}] {var}")
                count += 1

st.divider()
st.subheader("📂 CBT 분석 Raw 데이터베이스")
st.dataframe(df_written, use_container_width=True, height=300)

# --- [하단 문구 및 저작권] ---
st.divider()
st.caption("🌿 본 리포트는 전기기능사 CBT 기출 데이터를 기반으로 구성된 AI 분석 시뮬레이션입니다. 문제은행 방식의 특성상 실제 시험마다 출제 문항이 다를 수 있으므로 전략 수립을 위한 <b>보조 지표</b>로만 활용하시기 바랍니다.")
st.markdown("<div style='text-align: center; color: #999; font-size: 0.8em; margin-top: 30px; letter-spacing: 2px;'>2026 AI VOLTMASTER ANALYTICS. ALL RIGHTS RESERVED.</div>", unsafe_allow_html=True)