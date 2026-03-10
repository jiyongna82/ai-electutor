import streamlit as st
import pandas as pd
import os
from datetime import datetime

# 1. 페이지 설정
st.set_page_config(page_title="공지사항 | VoltMaster", page_icon="🔔", layout="wide")

# 2. 데이터 로드 함수
def load_notices():
    csv_path = 'notices.csv'
    if os.path.exists(csv_path):
        try:
            df = pd.read_csv(csv_path)
            df['date'] = pd.to_datetime(df['date'])
            df = df.sort_values(by='date', ascending=False)
            return df
        except Exception as e:
            st.error(f"데이터를 읽어오는 중 오류가 발생했습니다: {e}")
            return pd.DataFrame(columns=["category", "title", "content", "date"])
    else:
        return pd.DataFrame(columns=["category", "title", "content", "date"])

df_notices = load_notices()

# 3. 타이틀 및 상단 브랜딩
st.title("🔔 VoltMaster 공식 공지사항")
st.markdown("전력 운용 포털의 최신 소식과 시스템 업데이트 내역을 안내해 드립니다.")

st.warning("🚧 **[안내] 실시간 알림 엔진 및 DB 통합 작업 진행 중 (현재 공지 열람만 가능)**")
st.divider()

# 4. 고정 공지사항 (Pinned Notice - 항상 최상단)
with st.container(border=True):
    st.markdown("### 📌 [중요] VoltMaster 서비스 오픈 현황 및 향후 업데이트 일정")
    st.caption(f"작성일: {datetime.now().strftime('%Y-%m-%d')} | 작성자: **VoltMaster 운영팀**")
    
    st.markdown("""
    안녕하세요, 대한민국 전기인의 스마트한 파트너 **VoltMaster (ai-electutor.com)**입니다.
    
    공식 오픈과 함께 보내주신 많은 관심에 깊이 감사드립니다. VoltMaster는 현장 실무의 효율성을 극대화하고, 최고 난이도의 자격증 합격을 돕기 위해 단계별로 서비스를 오픈하고 있습니다. 현재 이용 가능한 서비스와 곧 선보일 업데이트 예정 기능을 안내해 드립니다.

    #### ✅ 현재 이용 가능한 서비스 (OPEN)
    가장 빠르고 정확한 실무 계산과, 기술사 합격을 위한 AI 심층 분석을 지금 바로 경험해 보세요.
    * **⚡ VoltMaster 홈**
    * **🧮 실무 전력 계산기:** 복잡한 수식 없이 현장에서 모바일로 즉시 결과를 도출하는 스마트 계산기
    * **🥇 건축전기설비기술사:** 105회~138회 빅데이터 기반 AI 심층 출제 시나리오 및 핵심 100선
    * **☕ 전기인의 핫플 & 트렌드:** 업계 최신 기술 동향 공유 및 선후배 전기인이 소통하는 커뮤니티

    #### 🚧 오픈 준비 중인 서비스 (COMING SOON)
    수험생을 위한 AI 튜터링과 현장 실무자를 위한 강력한 아카이브 기능이 현재 구축 중입니다.
    * **✨ AI 튜터 메인/통계:** 자격증별 최신 출제 트렌드 및 합격 지표 종합 대시보드
    * **🥈 전기기사 / 🥉 전기산업기사 / 🎖️ 전기기능사:** AI 핀셋 추출 리포트 및 맞춤형 튜터링
    * **🔍 KEC 스마트 검색기:** 방대하고 헷갈리는 한국전기설비규정(KEC)을 키워드로 빠르게 탐색
    * **📚 설비 아카이브 & 📝 현장 점검 양식:** 필수 기술 자료 및 최신 검측/안전 점검 포맷

    사용 중 개선이 필요하거나 추가를 원하는 기능이 있다면 아래 버튼을 적극 활용해 주시기 바랍니다. 여러분의 소중한 의견을 바탕으로 더욱 완벽한 서비스를 만들어가겠습니다.
    """)
    
    # 텍스트 대신 명확한 '페이지 링크' 컴포넌트 사용
    st.page_link("pages/9_request_board.py", label="💡 기능/자료 요청 게시판 바로가기", icon="🚀")

st.markdown("<br>", unsafe_allow_html=True)

# 5. 최신 업데이트 히스토리 (요약 기능 적용)
st.subheader("📑 최신 업데이트 히스토리")

if not df_notices.empty:
    recent_notices = df_notices.head(5)
    older_notices = df_notices.iloc[5:]

    # [최신 5개 출력]
    for idx, row in recent_notices.iterrows():
        date_str = row['date'].strftime('%Y-%m-%d')
        content = str(row['content'])
        
        with st.container(border=True):
            col_title, col_date = st.columns([4, 1])
            col_title.markdown(f"**[{row['category']}]** {row['title']}")
            col_date.markdown(f"<div style='text-align: right; color: gray;'><i>{date_str}</i></div>", unsafe_allow_html=True)
            
            # --- 본문 요약 로직 ---
            summary_limit = 150 
            
            if len(content) > summary_limit:
                st.markdown(content[:summary_limit] + "...")
                with st.expander("📖 본문 전체 보기", expanded=False):
                    st.markdown(content)
            else:
                st.markdown(content)

    st.markdown("<br>", unsafe_allow_html=True)

    # [과거 공지 펼쳐보기]
    if not older_notices.empty:
        with st.expander("➕ 이전 업데이트 이력 더보기 (6번~)", expanded=False):
            for idx, row in older_notices.iterrows():
                date_str = row['date'].strftime('%Y-%m-%d')
                st.markdown(f"**[{row['category']}]** {row['title']} | *{date_str}*")
                with st.popover("내용 보기"):
                    st.markdown(row['content'])
                st.divider()
else:
    st.info("현재 등록된 업데이트 히스토리가 없습니다.")

st.divider()
st.info("💡 **VoltMaster**는 전기 전문가들의 업무 효율을 위해 끊임없이 진화합니다.")

# --- 6. 관리자 모드 히든 아이콘 ---
st.markdown(
    """
    <div style="text-align: center; margin-top: 50px; opacity: 0.5;">
        <p style="color: gray; font-size: 12px;">
            © 2026 VoltMaster. All rights reserved. 
            <a href="javascript:window.location.href='/?manage=true'" target="_self" style="color:rgba(0,0,0,0); font-size:20px; text-decoration:none; cursor:pointer;">.</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True
)