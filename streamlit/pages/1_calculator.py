import streamlit as st
import os  

def main():
    st.set_page_config(page_title="전력기술 실무 계산 포털", layout="wide")
    
    # --- [디자인 설정] 화면 하단 및 구분선 여백 축소 ---
    st.markdown("""
        <style>
            /* 메인 컨테이너 최하단 여백 대폭 축소 */
            .block-container {
                padding-top: 1.5rem !important;
                padding-bottom: 1rem !important;
            }
            /* 가로 구분선(hr) 위아래 여백 축소 */
            hr {
                margin-top: 1.5rem !important;
                margin-bottom: 0.5rem !important;
            }
            /* 우측 상단 선택창 위치 미세 조정을 위한 스타일 */
            div[data-testid="stColumn"]:nth-child(2) {
                display: flex;
                flex-direction: column;
                justify-content: flex-start;
            }
        </style>
    """, unsafe_allow_html=True)
    
    # --- 데이터 정의 (마스터 리스트) ---
    calc_list = {
        "1단원. 전선 및 배선 (KEC 기반)": [
            "1-1. 전선 허용전류 산출기", "1-2. 전압강하 산출 및 적정 전선 굵기(SQ) 선정기",
            "1-3. 케이블 트레이 단면적 및 점적률(%) 계산기", "1-4. 전선관 굵기 선정기",
            "1-5. 접지선 굵기 산출기", "1-6. 중성선 굵기 산출기",
            "1-7. 지중 케이블 허용전류 보정계수 적용 계산기", "1-8. 단락 시 전선 허용 온도 도달 시간 계산기",
            "1-9. 케이블 포설 장력 및 측압 계산기", "1-10. 허용 접촉전압 및 보폭전압 계산기",
            "1-11. 고압/저압 부스덕트(Busduct) 규격 및 허용전류 산출기"
        ],
        "2단원. 수배전반 및 변압기": [
            "2-1. 변압기 용량 산출기", "2-2. 변압기 퍼센트 임피던스(%Z) 및 단락전류 계산기",
            "2-3. 변압기 효율 산출 및 최대 효율 조건 계산기", "2-4. 변압기 병렬운전 부하 분담률 계산기",
            "2-5. CT(변류기) 정격 및 부담(Burden) 선정기", "2-6. PT(계기용변압기) 정격 및 퓨즈 용량 선정기",
            "2-7. NGR(중성점 접지 저항기) 저항값 및 지락전류 제한 산출기", "2-8. 메인 차단기(VCB/ACB) 정격차단전류(kA) 선정기",
            "2-9. 배전반 모선(Busbar) 규격 및 허용전류 산출기", "2-10. 차단기 간 보호협조 및 선택차단 분석기",
            "2-11. 전력용 콘덴서 및 역률 개선 상세 분석기", "2-12. K-factor 적용 IT용 TR 발열량 산출기",
            "2-13. 고압 콘덴서 NVS 보호 및 SR 전압 상승 분석기"
        ],
        "3단원. 동력 및 전동기 부하": [
            "3-1. 3상 유도전동기 기동전류 및 기동 방식 설정기", "3-2. 전동기 역률 개선용 저압 진상콘덴서 용량 선정기",
            "3-3. 전동기 부하에 따른 차단기(MCCB) 및 EOCR 세팅치 산출기", "3-4. 인버터(VFD) 적용 시 고조파 발생량 및 필터 용량 계산기",
            "3-5. 전동기 토크(Torque) 및 출력(kW/HP) 변환기", "3-6. 양수기(펌프)용 전동기 소요 동력(kW) 산출기",
            "3-7. 기동 임피던스 및 계통 전압 안정성 분석", "3-8. 승강기(엘리베이터)용 전동기 소요 동력 산출기",
            "3-9. 전동기 효율 및 슬립(Slip) 산출기", "3-10. 전동기 발열량 및 필요 냉각 공기량 산출기"
        ],
        "4단원. 보호계전 및 전력품질 분석": [
            "4-1. 수변전계통 단락전류 및 차단용량 산출기", "4-2. 보호계전기(OCR/OCGR) 정정치 및 보호협조 분석기",
            "4-3. 변압기 돌입전류(Inrush) 및 OCR 오동작 검토기", "4-4. 고조파(Harmonics) 함유율(THD) 및 기기 영향 분석기",
            "4-5. 계통 임피던스 기반 정밀 전압강하 분석", "4-6. 순간 전압 강하(Voltage Sag) 및 장비 정지 위험 분석",
            "4-7. 1선 지락 사고 시 지락전류 및 대지전위 상승(EPR) 산출기", "4-8. 서지 보호 장치(SPD) 전압 보호 레벨 및 유효 거리 검토기",
            "4-9. 변압기 병렬운전 조건 및 순환전류 분석기", "4-10. 역률 개선용 콘덴서 용량 및 고조파 유입 방지(SR) 산출기",
            "4-11. 비상발전기-한전 전원 CTTS(무정전 절체) 동기 조건 분석기"
        ],
        "5단원. 비상전원 및 신재생에너지 (ESG)": [
            "5-1. 비상발전기 용량 산출 (RG/PG)", "5-2. 발전기 병렬운전 및 부하 분담 분석기",
            "5-3. 연료 공급 시스템 및 유류 탱크 용량 계산기", "5-4. UPS 축전지(배터리) 용량 및 백업 타임 산출기",
            "5-5. 태양광(PV) 발전 효율 및 수익 시뮬레이터", "5-6. 에너지 저장 장치(ESS) 피크컷 및 운용 효율 분석기",
            "5-7. 발전기 DPF 배압 및 재생 조건 분석기", "5-8. 고조파 함유율에 따른 발전기 손실 및 건전성 분석",
            "5-9. 신재생 연계형 마이크로그리드 안정성 검토기", "5-10. 탄소배출권 및 RE100 이행 지표 산출기"
        ],
        "6단원. 데이터센터 특화 설비 및 자동제어 시스템": [
            "6-1. FMS 기반 PUE 실시간 분석기", "6-2. 서버실 기류 차폐(Containment) 및 차압 분석기",
            "6-3. 외기 냉방(Free Cooling) 경제성 시뮬레이터", "6-4. STS(Static Transfer Switch) 고속 절체 분석기",
            "6-5. 서버 랙(Rack) 전력 밀도 및 LOP 관리기", "6-6. 조기 반응 화재 감지(VESDA) 농도 시퀀스 분석기",
            "6-7. 가스계 소화 밀폐도(Fan Integrity) 테스트 시뮬레이터", "6-8. 냉동기 대수 제어 및 델타T(ΔT) 효율 분석기",
            "6-9. 24/7 무탄소 에너지(CFE) 및 탄소 발자국 분석", "6-10. 액침 냉각(Immersion Cooling) 효율 및 에너지 분석",
            "6-11. DCIM 자산 배치 및 상면 하중 최적화 분석"
        ]
    }

    # --- 상단 레이아웃 (제목 및 우측 선택창) ---
    head_col, select_col = st.columns([8, 2])
    
    with head_col:
        st.markdown("### ⚡ 전력 계통 실무 계산 포털")
        st.markdown("<p style='color: #64748B; font-size: 0.95rem; margin-top: -10px;'>Professional Engineering Calculation Portal</p>", unsafe_allow_html=True)
    
    with select_col:
        # 우측 상단 드롭다운 메뉴 (사이드바와 동기화)
        st.markdown("""<style>div[data-testid="stSelectbox"] { margin-top: -5px; }</style>""", unsafe_allow_html=True)
        top_unit = st.selectbox("📖 단원 빠른 선택", list(calc_list.keys()), key="top_unit_sel")
        top_item = st.selectbox("🔍 계산기 바로가기", calc_list[top_unit], key="top_item_sel")

    # --- 사이드바 메뉴 (우측 상단 메뉴와 동기화) ---
    st.sidebar.header("📋 계산기 카테고리")
    # 세션 상태를 활용하여 양쪽 메뉴의 선택값을 일치시킴
    selected_unit = st.sidebar.selectbox("📖 단원 선택", list(calc_list.keys()), index=list(calc_list.keys()).index(top_unit))
    selected_item = st.sidebar.radio("🔍 세부 계산기 항목", calc_list[selected_unit], index=calc_list[selected_unit].index(top_item))

    st.divider()

    # --- 계산기 동적 실행 로직 ---
    try:
        # 사이드바와 상단 메뉴 중 마지막으로 변경된 값을 기준으로 실행
        active_item = selected_item 
        item_no = active_item.split('.')[0].strip()
        file_suffix = item_no.replace('-', '_')
        
        file_path = f"calculators/calc_{file_suffix}.py"
        
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                code = f.read()
            
            namespace = {}
            exec(code, namespace)
            
            if 'run_calc' in namespace:
                namespace['run_calc']()
                st.info("💡 **알림:** 본 계산 결과는 표준 공학 수식을 바탕으로 한 시뮬레이션입니다. 실제 현장 적용 시에는 반드시 전문 기술자와 상담하시기 바랍니다.")
            else:
                st.warning(f"⚠️ '{file_path}' 내부에 'run_calc()' 함수가 없습니다.")
        else:
            st.info(f"📂 **현황:** 현재 [{active_item}] 모듈을 준비 중입니다. (경로: {file_path})")

    except Exception as e:
        st.error(f"⚠️ 시스템 오류: {e}")

    # --- 하단 면책 조항 ---
    st.markdown("---")
    st.caption("""
        ⚠️ **Disclaimer** 본 시스템의 산출값은 실무 참고용이며 법적 효력이 없습니다. 
        모든 설계 및 운용 결정은 국가 표준(KEC 등)을 준수하고 전문 자격자의 검토를 거치시기 바랍니다.
    """)

if __name__ == "__main__":
    main()