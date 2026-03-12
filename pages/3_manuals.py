import streamlit as st

st.set_page_config(page_title="스마트 전력설비 아카이브", page_icon="📚", layout="wide")

# 웹 뷰어를 위한 세션 상태(Session State) 초기화
if 'selected_manual' not in st.session_state:
    st.session_state['selected_manual'] = None

def open_viewer(manual_name):
    st.session_state['selected_manual'] = manual_name

# 세련되고 묵직한 타이틀
st.title("📚 VoltMaster 전력설비 통합 기술 아카이브")

# 🚨 [수정된 부분] 방문객 친화적인 서비스 예정 안내 문구
st.warning("🚧 **[안내] 현재 주요 제조사별 전력 설비 매뉴얼 및 기술 문서 통합 작업이 진행 중입니다. (정식 서비스 오픈 예정)**\n\n*※ 아래 화면은 문서를 다운로드 없이 빠르고 편리하게 열람할 수 있는 '스마트 웹 뷰어' 기능의 데모(샘플) UI입니다.*")

st.markdown("현장에서 가장 많이 쓰이는 주요 제조사별 설비 매뉴얼을 **다운로드 없이 웹에서 바로 열람**할 수 있습니다.")
st.markdown("---")

# 화면을 좌우로 분할 (좌: 매뉴얼 목록 / 우: PDF 웹 뷰어)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📁 매뉴얼 카테고리")
    search_query = st.text_input("🔍 설비명 또는 제조사 검색 (예: LS일렉트릭, VCB)")
    
    tab1, tab2, tab3 = st.tabs(["⚡ 수배전 설비", "🔋 예비/무정전 전원", "❄️ 기계/방재 설비"])
    
    # [탭 1] 범용 수배전 설비
    with tab1:
        with st.expander("1. 특고압 차단기 및 개폐기 (VCB, ALTS, ASS)"):
            st.markdown("- **LS일렉트릭 VCB:** Susol 진공차단기 취급설명서")
            st.button("📖 VCB 매뉴얼 웹에서 보기", key="vcb_view", on_click=open_viewer, args=("LS일렉트릭 Susol VCB 취급설명서",))
            
            st.markdown("- **비츠로테크 ALTS:** 자동부하전환개폐기 조작 매뉴얼")
            st.button("📖 ALTS 매뉴얼 웹에서 보기", key="alts_view", on_click=open_viewer, args=("비츠로테크 ALTS 조작 매뉴얼",))

        with st.expander("2. 전력용 변압기 (Mold, Oil TR)"):
            st.markdown("- **효성중공업 몰드변압기:** 설치 및 유지보수 지침서")
            st.button("📖 몰드 TR 매뉴얼 웹에서 보기", key="tr_view", on_click=open_viewer, args=("효성중공업 몰드변압기 유지보수 지침서",))

        with st.expander("3. 저압 기기 (ACB, MCCB)"):
            st.markdown("- **현대일렉트릭 ACB:** 기중차단기 보호계전기(OCR) 세팅 가이드")
            st.button("📖 ACB 세팅 가이드 보기", key="acb_view", on_click=open_viewer, args=("현대일렉트릭 ACB OCR 세팅 가이드",))

    # [탭 2] 범용 예비/무정전 전원 설비
    with tab2:
        with st.expander("1. 비상발전기 (Diesel / Gas)"):
            st.markdown("- **커민스(Cummins) 디젤 발전기:** 제어판넬(PCC) 알람 코드 및 조치방법")
            st.button("📖 커민스 발전기 매뉴얼 보기", key="gen_view", on_click=open_viewer, args=("커민스 발전기 알람 코드 조치방법",))
            
            st.markdown("- **캐터필라(Caterpillar):** 정기 소모품 교체 및 점검 매뉴얼")

        with st.expander("2. 무정전 전원장치 (UPS)"):
            st.markdown("- **슈나이더(Schneider) Galaxy 시리즈:** UPS 절체 시퀀스 및 바이패스 조작법")
            st.button("📖 슈나이더 UPS 조작법 보기", key="ups_view", on_click=open_viewer, args=("슈나이더 Galaxy UPS 바이패스 조작법",))

    # [탭 3] 범용 기계/방재 설비
    with tab3:
        with st.expander("1. 냉각 및 항온항습 설비"):
            st.markdown("- **범양냉방 항온항습기:** 알람 이력 확인 및 필터 교체 가이드")
            st.button("📖 항온항습기 가이드 보기", key="hvac_view", on_click=open_viewer, args=("범양냉방 항온항습기 에러 조치 가이드",))

        with st.expander("2. 소방 및 가스계 소화설비"):
            st.markdown("- **화재수신기 (R형/P형):** 동방전자 R형 수신기 연동 정지 및 복구 매뉴얼")
            st.button("📖 수신기 조작 매뉴얼 보기", key="fire_view", on_click=open_viewer, args=("동방전자 R형 수신기 복구 매뉴얼",))

with col2:
    # 🌟 [수정된 부분] 괄호 안의 영업 비밀 문구 삭제
    st.subheader("🖥️ 스마트 웹 뷰어")
    
    if st.session_state['selected_manual']:
        st.success(f"현재 열람 중: **{st.session_state['selected_manual']}**")
        
        # 🌟 [수정된 부분] 광고 관련 내부 안내 텍스트 삭제
        st.markdown(
            f"""
            <div style="height: 600px; border: 2px solid #ccc; border-radius: 5px; background-color: #f9f9f9; display: flex; flex-direction: column; align-items: center; justify-content: center;">
                <h3 style="color: #666;">📄 PDF 뷰어 로딩 중...</h3>
                <p style="color: #888;">추후 이 영역에 {st.session_state['selected_manual']}의 실제 문서가 내장되어 표시됩니다.</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
    else:
        st.info("👈 왼쪽 목록에서 열람할 매뉴얼의 **'웹에서 보기'** 버튼을 클릭해 주세요.")
        st.markdown(
            """
            <div style="height: 600px; border: 2px dashed #ddd; border-radius: 5px; display: flex; align-items: center; justify-content: center;">
                <h4 style="color: #aaa;">매뉴얼이 이곳에 표시됩니다.</h4>
            </div>
            """,
            unsafe_allow_html=True
        )