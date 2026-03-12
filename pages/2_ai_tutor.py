import streamlit as st
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="AI Exam Intelligence", page_icon="📊", layout="wide")

# 2. 상단 헤더
st.title("📊 AI EXAM INTELLIGENCE")
st.markdown(f"<p style='font-size: 1.1em; color: #555;'>최신 기출 빅데이터를 분석하여 <b>{datetime.now().year}년도</b> 전기분야 자격증 출제 경향과 합격 전략을 제시합니다.</p>", unsafe_allow_html=True)
st.divider()

# ==========================================
# [1단락] 건축전기설비기술사
# ==========================================
with st.container(border=True):
    st.markdown("### 🥇 건축전기설비기술사 (Professional Engineer Electric)")
    st.write("**💡 AI 분석 리포트 요약:** 최근 대규모 데이터센터(IDC) 인프라 확충 트렌드가 강력하게 반영되고 있습니다. 수배전반 모선 이중화(ATS/CTTS) 및 변압기 효율과 관련된 실무 지향적 서술형 문항의 출제 가중치가 매우 높게 분석되었습니다.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("필기 합격률", "3.8%", "-0.4%")
    c2.metric("최종(면접) 합격률", "14.2%", "+1.5%")
    c3.metric("최근 응시 인원", "1,850명", "소폭 상승 추세")
    c4.metric("AI 예상 문제수", "총 100선", "분야별 핀셋 추출")
    c5.metric("직전회차 AI 적중률", "84.5%", "안정적")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 건축전기설비기술사 AI 분석 바로가기", use_container_width=True, key="btn_pe", type="primary"):
        st.switch_page("tutor/1_professional.py") # 파일 경로가 다를 경우 수정 필요

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# [2단락] 전기기사
# ==========================================
with st.container(border=True):
    st.markdown("### 🥈 전기기사 (Engineer Electricity)")
    st.write("**💡 AI 분석 리포트 요약:** KEC(한국전기설비규정) 시행 안정화에 따라, 필기와 실기 모두 '보호도체 단면적 산정' 및 '접지 저항' 관련 수치 계산 문항이 출제 임계치를 넘었습니다. 실기의 경우 수변전 단선도 해석이 합격의 당락을 가릅니다.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("필기 합격률", "22.4%", "+2.1%")
    c2.metric("최종(실기) 합격률", "16.8%", "-3.2%")
    c3.metric("최근 응시 인원", "58,210명", "지속 상승세")
    c4.metric("AI 예상 문제수", "총 350선", "필기300/실기50")
    c5.metric("직전회차 AI 적중률", "88.2%", "매우 높음")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 전기기사 AI 분석 바로가기", use_container_width=True, key="btn_eng"):
        st.switch_page("tutor/2_engineer.py") # 파일 경로가 다를 경우 수정 필요

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# [3단락] 전기산업기사
# ==========================================
with st.container(border=True):
    st.markdown("### 🥉 전기산업기사 (Industrial Engineer Electricity)")
    st.write("**💡 AI 분석 리포트 요약:** 필기에서 제어공학이 제외됨에 따라 회로이론의 배점이 높아졌습니다. 실기는 기사 시험보다 '시퀀스 및 논리회로' 도면 해석의 비중이 25% 이상 차지하므로 이에 대한 반복 훈련이 필수적입니다.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("필기 합격률", "20.1%", "-1.1%")
    c2.metric("최종(실기) 합격률", "15.3%", "+0.8%")
    c3.metric("최근 응시 인원", "32,450명", "보합세")
    c4.metric("AI 예상 문제수", "총 350선", "필기300/실기50")
    c5.metric("직전회차 AI 적중률", "86.7%", "상승 추세")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 전기산업기사 AI 분석 바로가기", use_container_width=True, key="btn_ind"):
        st.switch_page("tutor/3_industrial.py") # 파일 경로가 다를 경우 수정 필요

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# [4단락] 전기기능사
# ==========================================
with st.container(border=True):
    st.markdown("### 🎖️ 전기기능사 (Craftsman Electricity)")
    st.write("**💡 AI 분석 리포트 요약:** CBT 방식의 문제은행 특성상 과거 5개년 기출의 반복 비율이 60%를 넘습니다. 특히 '전기설비' 과목은 100% 암기 과목으로, AI가 추출한 KEC 개정 관련 배선/배관 규정만 숙지해도 고득점이 가능합니다.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("필기 합격률", "32.5%", "+3.4%")
    c2.metric("최종(실기) 합격률", "68.2%", "안정 유지")
    c3.metric("최근 응시 인원", "45,100명", "큰 폭 상승")
    c4.metric("AI 예상 문제수", "총 180선", "과목별 60제")
    c5.metric("직전회차 AI 적중률", "92.1%", "최고 수준")
    
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔍 전기기능사 AI 분석 바로가기", use_container_width=True, key="btn_cra"):
        st.switch_page("tutor/4_craftsman.py") # 파일 경로가 다를 경우 수정 필요

st.divider()
st.caption("🌱 본 리포트는 인공지능(AI)이 기출 빅데이터를 학습하여 예측한 분석 결과입니다. 실제 출제 경향과 다를 수 있으므로, 학습 전략 수립을 위한 보조 지표로만 가볍게 참고해 주시길 바랍니다.")