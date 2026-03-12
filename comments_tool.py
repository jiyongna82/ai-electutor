import streamlit as st
import pandas as pd
import os
import sys
from datetime import datetime
import time

# --- [경로 동기화 로직] ---
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
VENV_BIN_PATH = os.path.join(CURRENT_DIR, "venv", "bin")
if VENV_BIN_PATH not in sys.path:
    sys.path.append(VENV_BIN_PATH)

try:
    from bad_words import BAD_WORDS_LIST
except ImportError:
    BAD_WORDS_LIST = []

def render_board(vol_id):
    file_path = os.path.join(CURRENT_DIR, f"comments_{vol_id}.csv")

    # 1. 데이터 로드
    if os.path.exists(file_path):
        try: df = pd.read_csv(file_path)
        except: df = pd.DataFrame(columns=["date", "name", "comment"])
    else:
        df = pd.DataFrame(columns=["date", "name", "comment"])

    st.markdown("---")
    st.markdown("## 💬 VoltMaster 커뮤니티")

    # 2. 히든 관리자 연동 (지용님의 세션 변수 admin_logged_in 확인)
    is_admin = st.session_state.get('admin_logged_in', False)

    if is_admin:
        st.caption("🔧 **VoltMaster 관리자 모드:** 댓글 삭제 권한이 활성화되었습니다.")

    # 3. 댓글 입력 폼
    with st.container(border=True):
        st.write("이번 호 내용에 대해 궁금한 점이나 의견을 남겨주세요!")
        with st.form(key=f'form_{vol_id}', clear_on_submit=True):
            col_name, col_msg = st.columns([1, 3])
            with col_name:
                name = st.text_input("성함/닉네임", placeholder="닉네임")
            with col_msg:
                comment = st.text_area("의견", placeholder="궁금하신 사항을 물어보세요!", height=100)
            
            if st.form_submit_button("댓글 남기기"):
                if not name.strip() or not comment.strip():
                    st.warning("⚠️ 닉네임과 내용을 모두 입력해 주세요.")
                elif any(word in comment for word in BAD_WORDS_LIST):
                    st.error("🚫 부적절한 표현이 포함되어 등록할 수 없습니다.")
                elif not df.empty and (df.iloc[-1]['name'] == name and df.iloc[-1]['comment'] == comment):
                    st.warning("🛑 도배 방지: 동일한 내용을 연속해서 올릴 수 없습니다.")
                else:
                    new_row = pd.DataFrame([[datetime.now().strftime("%Y-%m-%d %H:%M:%S"), name, comment]], 
                                            columns=["date", "name", "comment"])
                    new_row.to_csv(file_path, mode='a', header=not os.path.exists(file_path), index=False)
                    st.success("✅ 의견이 등록되었습니다!")
                    time.sleep(0.5)
                    st.rerun()

    # 4. 리스트업 및 삭제 버튼 (관리자 전용)
    if not df.empty:
        st.markdown("### 최근 의견 리스트")
        for idx in range(len(df)-1, -1, -1):
            row = df.iloc[idx]
            with st.chat_message("user"):
                if is_admin:
                    c1, c2 = st.columns([6, 1])
                    with c1:
                        st.write(f"**{row['name']}** <small style='color:gray;'>({row['date']})</small>", unsafe_allow_html=True)
                        st.write(row['comment'])
                    with c2:
                        if st.button("🗑️", key=f"del_{vol_id}_{idx}", help="댓글 삭제"):
                            df = df.drop(idx).reset_index(drop=True)
                            df.to_csv(file_path, index=False)
                            st.rerun()
                else:
                    st.write(f"**{row['name']}** <small style='color:gray;'>({row['date']})</small>", unsafe_allow_html=True)
                    st.write(row['comment'])
    else:
        st.info("아직 의견이 없습니다. 첫 번째 댓글을 남겨보세요!")