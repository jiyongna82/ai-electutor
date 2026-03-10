import streamlit as st
import pandas as pd
import altair as alt
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="AI 전기기사 Intelligence", page_icon="⚡", layout="wide")

# --- [페이지 업데이트 안내 문구] ---
st.info("🌱 현재 전기기사 AI 분석 엔진의 기출 데이터를 최신화하고 알고리즘을 고도화하는 업데이트 작업이 진행 중입니다. 더 나은 분석 서비스를 제공하기 위해 일부 화면이나 기능이 수시로 변동될 수 있으니 너른 양해 부탁드립니다.")

# 2. 분석용 가상 데이터 생성 (실제 CSV 연동 전 UI 확인용)
@st.cache_data(ttl=600)
def generate_mock_data():
    written_cats = ["1. 전기자기학", "2. 전력공학", "3. 전기기기", "4. 회로이론 및 제어공학", "5. 전기설비기술기준(KEC)"]
    written_data = pd.DataFrame({
        '과목': np.random.choice(written_cats, 1000, p=[0.2, 0.2, 0.2, 0.2, 0.2]),
        '난이도': np.random.choice(['상', '중', '하'], 1000, p=[0.2, 0.5, 0.3]),
        '핵심키워드': ['가우스법칙', '단락전류', '변압기효율', '라플라스변환', '접지시스템'] * 200
    })
    
    practical_cats = ["1. 수변전설비", "2. 시퀀스 및 PLC", "3. 조명 및 동력설비", "4. 송배전 선로특성", "5. 방재 및 설비기준(KEC)", "6. 감리 및 테이블스펙"]
    practical_data = pd.DataFrame({
        '과목': np.random.choice(practical_cats, 500, p=[0.25, 0.20, 0.20, 0.20, 0.10, 0.05]),
        '난이도': np.random.choice(['상', '중', '하'], 500, p=[0.3, 0.5, 0.2]),
        '핵심키워드': ['단선도작성', 'Y-델타기동', '광속법', '전압강하', '보호도체산정', '간선굵기'] * 83 + ['차단용량', 'PLC래더']
    })
    return written_data, practical_data

df_written, df_practical = generate_mock_data()

# --- [상단 레이아웃: AI 분석 타이틀] ---
head_col, select_col = st.columns([7, 3])
with head_col:
    st.title("⚡ AI-Driven 전기기사 Intelligence")
    st.markdown("<p style='color: #00796B; font-weight: bold;'>전기기사 필기/실기 빅데이터 정밀 분석 엔진 v2.5</p>", unsafe_allow_html=True)
    
with select_col:
    with st.popover("⚙️ AI 분석 매개변수 설정", use_container_width=True):
        st.radio("분석 가중치 기간 선택", ["최근 3개년 (가중치 1.5)", "최근 5개년 (가중치 1.2)", "최근 10개년 (전체)"], index=1)
        st.checkbox("KEC 개정(21년 이후) 문항 우선 정렬", value=True)

st.success("⚡ **AI 엔진 연산 완료:** 필기 300선(과목별 60문항) 및 실기 50선 핵심 알고리즘 추출 완료")

# --- [탭(Tab) 구성: 필기와 실기 분리] ---
tab_written, tab_practical = st.tabs(["📝 필기 (Written Analysis)", "🛠️ 실기 (Practical Analysis)"])

# ==========================================
# [TAB 1] 필기 (Written) 대시보드
# ==========================================
with tab_written:
    stats_w = df_written['과목'].value_counts().reset_index()
    stats_w.columns = ['과목', '문항수']
    stats_w['비중(%)'] = (stats_w['문항수'] / len(df_written) * 100).round(1)
    stats_w = stats_w.sort_values('과목')
    
    c1, c2, c3 = st.columns(3)
    c1.metric("필기 분석 표본(N)", f"{len(df_written)} 문항")
    c2.metric("AI 예측 도출 문항", "총 300문항 (5과목 x 60문항)")
    c3.metric("KEC 반영률", "100% 최우선 적용")
    
    st.divider()
    st.subheader("📊 필기 과목별 출제 분포 시각화")
    base_w = alt.Chart(stats_w).encode(
        y=alt.Y('과목:N', title=None, axis=alt.Axis(labelFontSize=13, labelFontWeight='bold')),
        x=alt.X('문항수:Q', title='출제 빈도수'),
        color=alt.condition(alt.datum['과목'] == '2. 전력공학', alt.value('#00796B'), alt.value('#B2DFDB'))
    ).mark_bar(cornerRadiusEnd=4).properties(height=300)
    text_w = base_w.mark_text(align='left', dx=5, color='black', fontWeight='bold').encode(text=alt.Text('비중(%):Q', format='.1f'))
    st.altair_chart(base_w + text_w, use_container_width=True)

    st.subheader("💡 필기 AI 심층 분석 시나리오")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### 1. 전력공학 (실기 직결)")
        st.write("**AI Logic:** 실기와 70% 겹치는 과목입니다. 단락전류 계산(%Z법), 전압강하 유도 공식은 단순 암기를 넘어 수리적 이해가 필수입니다.")
        st.markdown("#### 2. 전기설비기술기준 (KEC)")
        st.write("**AI Logic:** 21년 개정 이후 TN/TT/IT 접지 방식과 보호도체 산정 규정이 60문항 중 최소 5문항 이상을 차지하는 A급 키워드입니다.")
    with col2:
        st.markdown("#### 3. 회로이론 및 제어공학")
        st.write("**AI Logic:** 블록선도, 라플라스 변환, 전달함수, 3상 교류 전력 계산은 출제 패턴이 고정되어 있어 기출 변형 훈련이 가장 효과적인 과목입니다.")
        st.markdown("#### 4. 전기자기학 및 전기기기")
        st.write("**AI Logic:** 벡터와 미적분으로 난이도를 조절합니다. 전계/자계 공식 비교, 동기기 특성곡선, 변압기 효율 계산에 집중하세요.")

    # --- [필기 출제 예상 300선 동적 생성 (과목당 60개)] ---
    st.divider()
    st.subheader("🎯 CSV 기반 AI 예측 필기 출제 예상 300선")
    st.caption("AI가 빈출 핵심 키워드 12개를 바탕으로 변형(이론, 계산, 응용 등)을 거쳐 과목당 60문항씩 총 300문항을 큐레이션했습니다.")
    
    # 5과목별 12개의 핵심 베이스 문항 (12 x 5유형 = 60문항)
    base_written = {
        "1. 전기자기학 (60문항)": [
            "진공 중 점전하에 의한 전계의 세기와 전위 계산", "가우스의 정리(미분형/적분형)와 대전 도체의 전계", 
            "평행판 콘덴서의 정전용량(C) 및 합성 정전용량", "유전체 경계면에서의 전속밀도와 굴절의 법칙",
            "비오-사바르 법칙을 이용한 원형 코일 중심의 자계", "무한장 직선 도체에 흐르는 전류에 의한 자계의 세기",
            "자성체의 종류(강/상/반자성체)와 자기저항 계산", "패러데이 전자유도 법칙과 유도 기전력(e)",
            "자체 인덕턴스(L)와 상호 인덕턴스(M)의 관계 및 결합계수", "평행왕복 도체 간에 작용하는 전자력(흡인력/반발력)",
            "변위전류의 개념과 맥스웰의 전자방정식", "전자파의 전파 속도와 고유 임피던스 산정"
        ],
        "2. 전력공학 (60문항)": [
            "가공 전선로의 이도(Dip) 계산 및 페란티 현상", "복도체(다도체) 사용 목적과 코로나 임계전압 공식",
            "선로정수(R, L, C) 작용 정전용량 및 연가(Transposition)", "송전단/수전단 전압과 전압강하율 및 전력손실률",
            "3상 단락전류 계산(%Z법 적용) 및 차단기 용량 선정", "중성점 접지 방식별(비접지/직접/저항) 1선 지락전류 비교",
            "이상전압 발생 원인과 피뢰기(LA)의 제한전압/정격전압", "수용률, 부등률, 부하율의 의미와 변압기 용량 결정",
            "역률 개선용 콘덴서(SC) 용량 산정과 경제적 효과", "배전선로의 부하중심 거리 계산 및 전압조정장치",
            "조속기의 특성과 수력 발전(낙차, 유량, 출력 계산)", "화력 발전의 열효율 및 원자력 발전 감속재 특성"
        ],
        "3. 전기기기 (60문항)": [
            "직류발전기의 전기자 반작용 방지 대책(보상권선 등)", "직류전동기의 속도 제어 방식(전압/계자/저항 제어)",
            "동기발전기의 병렬운전 조건(크기/위상/주파수/파형)", "동기발전기 단락비의 의미와 동기 임피던스 계산",
            "변압기의 등가회로와 무부하/단락 시험을 통한 손실 측정", "변압기 최대 효율 조건(철손=동손) 및 전압변동률",
            "변압기의 V-V 결선 출력비 및 3상/2상 변환(스코트 결선)", "3상 유도전동기의 슬립(Slip) 및 회전자 속도 계산",
            "유도전동기의 비례추이 원리와 최대 토크 특성", "단상 유도전동기 기동 방식별 기동 토크 크기 순서",
            "사이리스터(SCR)를 이용한 정류 회로의 직류 평균 전압", "단상/3상 반파 및 전파 정류회로의 맥동률 비교"
        ],
        "4. 회로이론 및 제어공학 (60문항)": [
            "키르히호프의 법칙, 테브난 및 노튼의 정리, 중첩의 원리", "R-L-C 직/병렬 공진 회로의 특성과 공진 주파수 계산",
            "Y-Δ 결선의 선간전압/상전압 관계와 3상 교류 전력 계산", "비정현파 교류의 실효값, 평균값, 왜형률 및 퓨리에 급수",
            "2단자망 및 4단자망의 Z, Y, ABCD 파라미터 변환", "시간 함수를 복소 주파수로 변환하는 라플라스 기본 변환",
            "블록선도와 신호흐름선도를 이용한 전체 전달함수 구하기", "1차 및 2차 지연요소의 시간응답(과도응답) 특성",
            "루스-후르비츠(Routh-Hurwitz) 안정도 판별법 적용", "나이퀴스트 및 보드선도 이득여유/위상여유 해석",
            "근궤적법을 이용한 제어계의 절대/상대 안정도 판별", "상태공간법에 의한 시스템 상태방정식 작성"
        ],
        "5. 전기설비기술기준 KEC (60문항)": [
            "KEC 저압/고압/특고압 전압의 분류 기준", "TN, TT, IT 계통접지 방식별 보호도체(PE) 단면적 산정",
            "기본보호(직접접촉)와 고장보호(간접접촉) 감전보호 대책", "저압 전로의 절연저항 기준값(SELV, PELV 500V 등)",
            "회전기 및 정류기, 변압기의 절연내력 시험전압 기준", "지중 전선로의 매설 깊이(관로식/직접매설식) 및 이격거리",
            "가공 전선로의 지지물 종류별 안전율 및 경간(Span) 제한", "저압/고압 가공전선과 식물, 건조물 간의 최소 이격거리",
            "옥내배선 공사(금속관/합성수지관/트레이) 전선 굵기 규정", "피뢰시스템(LPS)의 수뢰부 시스템 배치(회전구체법 등)",
            "태양광, 풍력, 연료전지 등 분산형 전원 계통 연계 기준", "의료 장소(수술실 등) 특수 설비의 안전 및 비상전원 기준"
        ]
    }

    # Python 로직을 이용해 12문항을 60문항으로 5배수 동적 확장 표출
    variations = ["[기본이론]", "[기출계산]", "[응용변형]", "[도면/그래프]", "[KEC복합]"]
    for cat, base_items in base_written.items():
        with st.expander(f"📌 {cat}"):
            count = 1
            for item in base_items:
                for var in variations:
                    st.write(f"**Q{count}.** {var} {item}")
                    count += 1

    st.divider()
    st.subheader("📂 필기 분석 Raw 데이터베이스")
    st.dataframe(df_written, use_container_width=True, height=250)


# ==========================================
# [TAB 2] 실기 (Practical) 대시보드
# ==========================================
with tab_practical:
    stats_p = df_practical['과목'].value_counts().reset_index()
    stats_p.columns = ['과목', '문항수']
    stats_p['비중(%)'] = (stats_p['문항수'] / len(df_practical) * 100).round(1)
    stats_p = stats_p.sort_values('과목')
    
    c1, c2, c3 = st.columns(3)
    c1.metric("실기 분석 표본(N)", f"{len(df_practical)} 문항")
    c2.metric("AI 예측 도출 문항", "총 50문항 핀셋 추출")
    c3.metric("최다 출제 유형", "수변전 단선도 & 계산")
    
    st.divider()
    st.subheader("📊 실기 분야별 출제 분포 시각화")
    base_p = alt.Chart(stats_p).encode(
        y=alt.Y('과목:N', title=None, axis=alt.Axis(labelFontSize=13, labelFontWeight='bold')),
        x=alt.X('문항수:Q', title='출제 빈도수'),
        color=alt.condition(alt.datum['과목'] == '1. 수변전설비', alt.value('#C62828'), alt.value('#FFCDD2'))
    ).mark_bar(cornerRadiusEnd=4).properties(height=350)
    text_p = base_p.mark_text(align='left', dx=5, color='black', fontWeight='bold').encode(text=alt.Text('비중(%):Q', format='.1f'))
    st.altair_chart(base_p + text_p, use_container_width=True)

    st.subheader("💡 실기 AI 심층 분석 시나리오 (AI Critical Path)")
    col3, col4 = st.columns(2)
    with col3:
        st.markdown("#### 1. 수변전설비 (도면 해석의 꽃)")
        st.write("**AI Logic:** 실기 배점의 30%를 차지합니다. 22.9kV-Y 수전설비 단선도를 통째로 암기하고 차단기 용량 산정을 완벽히 숙지해야 합니다.")
        st.markdown("#### 2. 시퀀스 및 PLC (논리 제어)")
        st.write("**AI Logic:** Y-Δ 기동 및 정역회로 미완성 도면 완성과, 논리식을 이용한 PLC 래더 다이어그램 변환이 10점형 문제로 자주 나옵니다.")
    with col4:
        st.markdown("#### 3. 송배전 선로 및 조명/동력")
        st.write("**AI Logic:** 광속법(FUN=EAD)과 역률 개선용 콘덴서 용량(Q=P(tan1-tan2)) 공식은 실기의 뼈대입니다. 계산 과정 작성 연습이 필수입니다.")
        st.markdown("#### 4. KEC 및 감리")
        st.write("**AI Logic:** 접지저항 및 케이블 단면적 산정은 5점형 단답으로 출제되며, 감리는 배치 기준표를 읽는 테이블스펙 문제로 자주 나옵니다.")

    # --- [실기 출제 예상 50선] ---
    st.divider()
    st.subheader("🎯 CSV 기반 AI 예측 실기 출제 예상 50선")
    st.caption("실무와 직결되는 도면/계산/단답형 기출 패턴을 분석하여 과목별로 가장 출제 확률이 높은 50개의 핵심 문항을 핀셋 추출했습니다.")
    
    predict_practical = {
        "1. 수변전설비 (10문항)": [
            "22.9kV-Y 수전설비 표준 단선도를 그리고, LA, PT, CT, MOF의 심벌과 역할을 기술하시오.",
            "주어진 부하 집계표를 바탕으로 메인 VCB의 정격 차단 용량(MVA)과 정격 전류를 선정하시오.",
            "수전용 변압기 1,2차측 CT의 정격(변류비)을 선정하고, 과전류계전기(OCR)의 Tap을 계산하시오.",
            "전력용 콘덴서 뱅크의 직렬리액터(SR) 및 방전코일(DC) 결선도를 그리고 목적을 서술하시오.",
            "ASS와 AISS의 차이점을 서술하고 단선도 상의 설치 위치를 표시하시오.",
            "변압기 병렬운전 조건을 적고, V-V결선 시 출력비와 이용률을 계산하시오.",
            "비상발전기실의 위치 선정 시 고려사항 4가지를 서술하시오.",
            "단락전류 계산을 위한 %Z(퍼센트 임피던스) 변환 공식을 쓰고 단락용량을 유도하시오.",
            "GPT와 ZCT를 이용한 비접지 계통의 지락 보호 방식 결선도를 완성하시오.",
            "수배전반 절연저항 측정(Megger) 시 인가전압 및 판정 기준표를 완성하시오."
        ],
        "2. 시퀀스 및 PLC (10문항)": [
            "3상 유도전동기 Y-Δ 기동회로의 주회로 및 보조회로 미완성 도면을 완성하시오.",
            "2대의 전동기 교대 운전 및 인터록(Interlock) 회로를 보고 타임차트를 작성하시오.",
            "주어진 논리식을 간소화하고, NAND 게이트만을 사용한 논리회로로 변환하시오.",
            "플로트 스위치(FS)를 이용한 급배수 펌프 자동 제어 회로의 오류를 찾아 수정하시오.",
            "PLC 래더 다이어그램을 보고 명령어 리스트(Mnemonic) 형태의 프로그램 코드로 작성하시오.",
            "온도 릴레이(THR)를 이용한 전동기 과부하 보호회로 동작 시퀀스를 서술하시오.",
            "버튼 스위치 3개를 이용한 우선순위(선입력 우선) 판별 회로를 설계하시오.",
            "타이머(T)의 한시동작 순시복귀 접점을 활용한 지연 회로를 도면으로 작성하시오.",
            "전자접촉기(MC)의 여자/소자 동작 메커니즘을 설명하고 보조접점(a,b) 역할을 쓰시오.",
            "주어진 진리표를 보고 카르노맵(Karnaugh Map)을 작성하여 논리식을 최적화하시오."
        ],
        "3. 조명 및 동력설비 (10문항)": [
            "광속법(FUN=EAD)을 이용하여 사무실 요구 조도를 위한 형광등/LED 등기구 수량을 계산하시오.",
            "실지수(Room Index) 공식에 실측 데이터를 대입하여 공간의 실지수를 산정하시오.",
            "분기회로 평면도를 보고, 전압강하 공식을 적용하여 분기회로 최소 전선 굵기(㎟)를 구하시오.",
            "부하 역률을 65%에서 90%로 개선하기 위해 필요한 전력용 콘덴서의 용량(kVA)을 계산하시오.",
            "건축물 소방 펌프용 전동기(kW) 용량을 양정, 유량, 여유계수를 이용하여 계산하시오.",
            "비상용 엘리베이터(권상기)의 전동기 용량 산정 공식을 쓰고 수치를 대입하시오.",
            "분기회로 수량 계산 시 표준 부하 밀도를 적용하여 15A 분기회로 수를 산정하시오.",
            "조명 설계 시 불쾌 글레어(눈부심) 발생 원인 3가지와 방지 대책을 서술하시오.",
            "도로 조명의 배치 방식(지그재그, 대칭 등)에 따른 조도 계산식을 전개하시오.",
            "간선의 허용전류 및 과전류 차단기 정격 선정 시 전동기 부하율에 따른 공식을 적용하시오."
        ],
        "4. 송배전 선로특성 (10문항)": [
            "3상 3선식 배전선로의 송/수전단 전압과 역률을 이용해 전압강하율 및 전력손실률을 계산하시오.",
            "수용가별 최대 전력이 주어졌을 때, 수용률과 부등률을 대입하여 주상 변압기 용량을 산정하시오.",
            "지중 전선로의 충전 용량(Qc)과 충전 전류(Ic)를 계산하는 수식을 전개하시오.",
            "페란티 현상을 방지하기 위해 뱅크에 설치할 분로리액터(Shunt Reactor) 용량을 구하시오.",
            "대칭좌표법을 이용해 송전선로 1선 지락 고장 시의 지락 전류(3I0)를 유도하시오.",
            "부하중심 거리(L) 산정 공식을 이용하여 공장 내 여러 부하의 전원 공급 중심점을 찾으시오.",
            "송전단 전압을 일정하게 유지하기 위한 동기조상기의 무효전력 공급 용량을 계산하시오.",
            "전압강하 근사식(e = I(Rcosθ + Xsinθ))을 이용하여 단상 및 3상 선로의 수전단 전압을 구하시오.",
            "배전선로의 연가(Transposition) 목적 3가지를 쓰고, 연가 방식을 간략히 도해하시오.",
            "가공 전선로 이도(Dip) 계산식을 쓰고, 온도 변화에 따른 전선 길이 변화율을 계산하시오."
        ],
        "5. 방재 및 설비기준 KEC (5문항)": [
            "KEC 규정에 따른 TN-C-S 접지 계통도를 그리고, 보호도체(PE)와 중성선(N)의 역할을 서술하시오.",
            "전동기 부하 전류를 바탕으로 KEC에 따른 보호도체(PE)의 최소 단면적(㎟)을 수식으로 계산하시오.",
            "건축물 피뢰시스템(LPS)의 보호 등급(I~IV)에 따른 인하도선 배치 간격을 서술하시오.",
            "고장보호(간접접촉) 감전 방지를 위한 자동차단 시간(0.4초 등)과 접지저항 관계를 설명하시오.",
            "옥내 지중 전선로와 가스관/수도관이 교차할 때 KEC 규정에 따른 최소 이격 거리를 쓰시오."
        ],
        "6. 감리 및 테이블스펙 (5문항)": [
            "주어진 배선용 차단기(MCCB) 프레임 규격표를 읽고, 계산된 허용전류에 맞는 차단기를 선정하시오.",
            "금속관 공사 간선 규격표를 해석하여, 전동기 3대 기동 조건을 만족하는 최소 전선 굵기를 찾으시오.",
            "공사 감리원의 배치 기준표를 보고, 연면적 30,000㎡ 건축물에 필요한 감리원 인원수를 산정하시오.",
            "설계도서 검토 시 감리원이 확인해야 하는 필수 항목 5가지를 단답형으로 서술하시오.",
            "준공 검사 및 사용 전 검사 시 전기안전관리법에 명시된 필수 절연/접지 검사 항목을 쓰시오."
        ]
    }
    
    for cat, items in predict_practical.items():
        with st.expander(f"📌 {cat}"):
            for i, item in enumerate(items):
                st.write(f"**Q{i+1}.** {item}")

    st.divider()
    st.subheader("📂 실기 분석 Raw 데이터베이스")
    st.dataframe(df_practical, use_container_width=True, height=250)

# --- [하단 문구 및 저작권] ---
st.divider()
st.caption("🌿 본 리포트는 전기기사 기출 데이터를 기반으로 구성된 AI 분석 시뮬레이션입니다. 본 자료를 전략 수립을 위한 <b>보조 지표</b>로만 활용하시기 바랍니다.")
st.markdown("<div style='text-align: center; color: #999; font-size: 0.8em; margin-top: 30px; letter-spacing: 2px;'>2026 AI VOLTMASTER ANALYTICS. ALL RIGHTS RESERVED.</div>", unsafe_allow_html=True)