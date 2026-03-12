import streamlit as st
import pandas as pd
from datetime import datetime
import os

def run_admin_notice():
    st.title("🔐 관리자 전용: 공지사항 마스터")
    st.markdown("공지사항의 작성, 수정, 삭제를 통합 관리합니다.")

    # --- [중요] 모든 세션 상태 초기화를 '로그인 체크' 보다 위로 올립니다 ---
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False
    if "edit_mode" not in st.session_state:
        st.session_state.edit_mode = False
    if "edit_index" not in st.session_state:
        st.session_state.edit_index = None

    # 1. 로그인 체크 (이제 아래에서 edit_mode를 참조해도 에러가 나지 않습니다)
    if not st.session_state.admin_logged_in:
        password = st.text_input("관리자 비밀번호를 입력하고 엔터를 치세요", type="password")
        
        if password:
            if password == "volt1234": 
                st.session_state.admin_logged_in = True
                st.rerun() 
            else:
                st.error("비밀번호가 틀렸습니다.")
        
        st.info("비밀번호 입력 후 [Enter] 키를 누르면 바로 접속됩니다.")
        return # 로그인 전에는 여기까지만 실행하고 멈춤

    # CSV 로드 함수
    csv_path = 'notices.csv'
    def get_df():
        if os.path.exists(csv_path):
            return pd.read_csv(csv_path)
        return pd.DataFrame(columns=["category", "title", "content", "date"])

    df = get_df()

    # 2. 작성/수정 폼
    # 수정 모드일 경우 기존 데이터를 폼에 채워넣음
    form_title = "📝 공지사항 수정" if st.session_state.edit_mode else "📝 새 공지 작성"
    submit_label = "공지사항 업데이트 🔄" if st.session_state.edit_mode else "공지사항 등록 🚀"

    with st.form("notice_form", clear_on_submit=not st.session_state.edit_mode):
        st.subheader(form_title)
        
        # 수정 모드 시 기본값 설정
        default_cat = "공지"
        default_title = ""
        default_content = ""
        default_date = datetime.now()

        if st.session_state.edit_mode and st.session_state.edit_index is not None:
            row = df.iloc[st.session_state.edit_index]
            default_cat = row['category']
            default_title = row['title']
            default_content = row['content'].replace("  \n", "\n") # 마크다운 줄바꿈 복원
            default_date = datetime.strptime(row['date'], "%Y-%m-%d")

        col1, col2 = st.columns([1, 3])
        with col1:
            category = st.selectbox("카테고리", ["공지", "업데이트", "점검", "안내", "이벤트"], 
                                    index=["공지", "업데이트", "점검", "안내", "이벤트"].index(default_cat))
        with col2:
            title = st.text_input("공지 제목", value=default_title)
            
        content = st.text_area("내용", value=default_content, height=200)
        date = st.date_input("게시 일자", value=default_date)
        
        col_btn1, col_btn2 = st.columns([1, 5])
        submit = col_btn1.form_submit_button(submit_label)
        
        if st.session_state.edit_mode:
            if col_btn2.form_submit_button("수정 취소 ❌"):
                st.session_state.edit_mode = False
                st.session_state.edit_index = None
                st.rerun()

    if submit:
        if title and content:
            new_row = {
                "category": category,
                "title": title,
                "content": content.replace("\n", "  \n"),
                "date": date.strftime("%Y-%m-%d")
            }
            
            if st.session_state.edit_mode:
                # 수정 로직
                df.iloc[st.session_state.edit_index] = new_row
                st.session_state.edit_mode = False
                st.session_state.edit_index = None
            else:
                # 신규 등록 로직 (맨 위에 추가)
                df = pd.concat([pd.DataFrame([new_row]), df], ignore_index=True)
            
            df.to_csv(csv_path, index=False, encoding='utf-8-sig')
            st.success("✅ 처리가 완료되었습니다!")
            st.rerun()

    # 3. 목록 출력 및 편집 컨트롤
    st.markdown("---")
    st.subheader("📂 공지사항 목록 편집")
    
    if not df.empty:
        # 순번 표시용 데이터프레임 복사
        display_df = df.copy()
        total_count = len(display_df)
        display_df.insert(0, 'No.', range(total_count, 0, -1))
        
        # 헤더
        cols = st.columns([0.5, 1, 3, 1.2, 1.2])
        cols[0].markdown("**No.**")
        cols[1].markdown("**카테고리**")
        cols[2].markdown("**제목**")
        cols[3].markdown("**날짜**")
        cols[4].markdown("**관리**")
        st.divider()

        # 목록 행
        for idx, row in display_df.iterrows():
            r_cols = st.columns([0.5, 1, 3, 1.2, 1.2])
            r_cols[0].write(row['No.'])
            r_cols[1].write(row['category'])
            r_cols[2].write(row['title'])
            r_cols[3].write(row['date'])
            
            # 수정/삭제 버튼을 한 열에 배치
            btn_col1, btn_col2 = r_cols[4].columns(2)
            if btn_col1.button("📝", key=f"edit_{idx}", help="수정"):
                st.session_state.edit_mode = True
                st.session_state.edit_index = idx
                st.rerun()
                
            if btn_col2.button("🗑️", key=f"del_{idx}", help="삭제"):
                df = df.drop(idx).reset_index(drop=True)
                df.to_csv(csv_path, index=False, encoding='utf-8-sig')
                st.rerun()
    else:
        st.info("등록된 공지사항이 없습니다.")

if __name__ == "__main__":
    run_admin_notice()