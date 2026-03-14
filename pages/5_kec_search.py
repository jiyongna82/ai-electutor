import streamlit as st

st.set_page_config(page_title="KEC 스마트 검색기", page_icon="🔍", layout="wide")

# 선택된 법규 조항을 기억하는 세션 상태 초기화
if 'selected_kec' not in st.session_state:
    st.session_state['selected_kec'] = None

def view_kec(clause_id):
    st.session_state['selected_kec'] = clause_id

st.title("🔍 KEC (한국전기설비규정) 스마트 검색기")

# 🚨 [추가된 부분] 최상단 서비스 예정 안내 문구
st.warning("🚧 **[안내] 현재 KEC 조항 데이터베이스 구축 및 맞춤형 검색 알고리즘 연동 작업이 진행 중입니다. (정식 서비스 오픈 예정)**\n\n*※ 아래 화면은 출시 예정인 기능의 데모(샘플) 버전입니다.*")

st.markdown("현장에서 헷갈리는 전기 규정을 키워드 하나로 빠르게 찾고, **실무 적용 가이드**까지 한 번에 확인하세요.")

# 💰 [수익화 포인트] 상단 배너
st.info("📢 [광고 배너 영역] 검색창 바로 위, 클릭률이 가장 높은 프리미엄 광고 자리입니다.")

# 1. 상단: 스마트 검색창 및 핫 키워드
col_search, col_hot = st.columns([2, 1])
with col_search:
    search_keyword = st.text_input("찾으시는 규정의 키워드나 조항 번호를 입력하세요. (예: 접지, 절연저항, 142.5)")
with col_hot:
    st.markdown("<br>", unsafe_allow_html=True)
    st.button("🔍 '접지시스템' 빠른 검색", use_container_width=True)

st.markdown("---")

# 화면 분할 (좌: 검색 결과 리스트 / 우: 상세 조항 및 실무 해설)
col1, col2 = st.columns([1, 1.2])

with col1:
    st.subheader("📋 검색 결과 목록")
    
    # 임시 샘플 데이터
    st.markdown("**(샘플) '접지' 관련 규정 검색 결과**")
    
    with st.container(border=True):
        st.markdown("**KEC 142.5** | 접지시스템의 시설")
        st.button("📖 조항 및 실무 해설 보기", key="kec_142", on_click=view_kec, args=("KEC 142.5",))
        
    with st.container(border=True):
        st.markdown("**KEC 232.3** | 배선설비의 이격거리 (케이블 트레이 등)")
        st.button("📖 조항 및 실무 해설 보기", key="kec_232", on_click=view_kec, args=("KEC 232.3",))

    with st.container(border=True):
        st.markdown("**KEC 502.1** | 태양광 발전설비의 접지")
        st.button("📖 조항 및 실무 해설 보기", key="kec_502", on_click=view_kec, args=("KEC 502.1",))

with col2:
    st.subheader("📜 규정 원문 및 현장 가이드")
    
    if st.session_state['selected_kec'] == "KEC 142.5":
        st.success("✅ **KEC 142.5 : 접지시스템의 시설**")
        with st.container(border=True):
            st.markdown("#### ⚖️ KEC 원문")
            st.markdown("""
            1. 접지극은 동결깊이를 감안하여 시설하되, 고압 이상의 전기설비와 변압기 중성점 접지에 의하여 시설하는 접지극은 지표면으로부터 0.75m 이상 깊은 곳에 매설하여야 한다.
            2. 접지도체는 지하 0.75m부터 지표 상 2m까지 부분은 합성수지관 등으로 덮어야 한다.
            """)
            st.markdown("---")
            st.markdown("#### 💡 현장 실무 가이드 (포털 독점 제공)")
            st.markdown("""
            * **적용 팁:** 데이터센터나 대형 플랜트 신축 현장에서는 개별 접지보다 **통합 접지 시스템(공통 접지)**을 주로 적용합니다. 
            * **체크 포인트:** 피뢰설비용 접지와 통신용 접지, 전력용 접지가 지하에서 등전위 본딩이 확실하게 되었는지 도면 검토 시 반드시 확인해야 합니다. 감리 업무 시 접지 저항계로 측정할 때 테스트 단자함(T/B) 위치를 사전에 파악해 두세요.
            """)
            
        # 💰 우측 하단 광고
        st.markdown("<br>", unsafe_allow_html=True)
        st.warning("📢 [광고 배너 영역] 법규를 주의 깊게 읽는 동안 노출되는 하단 배너입니다.")
        
    elif st.session_state['selected_kec'] == "KEC 502.1":
        st.success("✅ **KEC 502.1 : 태양광 발전설비의 접지**")
        with st.container(border=True):
            st.markdown("#### ⚖️ KEC 원문")
            st.markdown("태양광전지 모듈, 프레임 및 지지물은 규정에 따라 접지하여야 한다. (이하 생략)")
            st.markdown("---")
            st.markdown("#### 💡 현장 실무 가이드 (포털 독점 제공)")
            st.markdown("""
            * **적용 팁:** 대용량(예: 250kW급 이상) 태양광 설비 시공 시, 모듈 프레임 간의 접지 본딩(Jumper) 누락이 잦습니다. 인버터(PCS) 외함 접지와 별도로 어레이 구조물 전체가 등전위가 되도록 시공 상태를 체크하세요.
            """)
            
    else:
        st.info("👈 왼쪽 검색 결과에서 확인하고 싶은 **'조항 보기'** 버튼을 클릭해 주세요.")
        st.markdown(
            """
            <div style="height: 400px; border: 2px dashed #ddd; border-radius: 5px; display: flex; align-items: center; justify-content: center;">
                <h4 style="color: #aaa;">법규 원문과 실무 해설이 이곳에 표시됩니다.</h4>
            </div>
            """,
            unsafe_allow_html=True
        )