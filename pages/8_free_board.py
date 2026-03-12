import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
import json
from bad_words import check_bad_words

# 1. 페이지 설정
st.set_page_config(page_title="자유게시판 | VoltMaster", page_icon="💬", layout="wide")

# 2. 데이터 및 세션 초기화
CSV_PATH = 'free_board.csv'
POST_COOLDOWN = 120 

if "voted_posts" not in st.session_state:
    st.session_state.voted_posts = set()
if "last_post_time" not in st.session_state:
    st.session_state.last_post_time = None
if "edit_post_id" not in st.session_state:
    st.session_state.edit_post_id = None
if "expanded_post_id" not in st.session_state:
    st.session_state.expanded_post_id = None

# --- 데이터 처리 함수 ---
def load_posts():
    if os.path.exists(CSV_PATH):
        try:
            df = pd.read_csv(CSV_PATH)
            df['date'] = pd.to_datetime(df['date'])
            return df
        except:
            return pd.DataFrame(columns=["id", "author", "title", "content", "date", "likes"])
    return pd.DataFrame(columns=["id", "author", "title", "content", "date", "likes"])

def handle_like_callback(post_id):
    df = load_posts()
    df.loc[df['id'] == post_id, 'likes'] += 1
    df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
    st.session_state.voted_posts.add(post_id)
    st.session_state.expanded_post_id = post_id

def delete_post(post_id):
    df = load_posts()
    df = df[df['id'] != post_id].reset_index(drop=True)
    df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')

def update_post_content(post_id, new_title, new_content):
    df = load_posts()
    df.loc[df['id'] == post_id, 'title'] = new_title
    df.loc[df['id'] == post_id, 'content'] = new_content.replace("\n", "  \n")
    df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')

def save_post(author, title, content):
    is_admin = st.session_state.get("admin_logged_in", False)
    if not is_admin and st.session_state.last_post_time:
        elapsed = (datetime.now() - st.session_state.last_post_time).total_seconds()
        if elapsed < POST_COOLDOWN:
            return False, f"🕒 도배 방지 중입니다."
    
    author_to_check = author if author.strip() else "익명"
    df = load_posts()
    new_id = int(df['id'].max() + 1) if not df.empty else 1
    new_post = pd.DataFrame([{
        "id": new_id, "author": author_to_check, "title": title,
        "content": content.replace("\n", "  \n"), "date": datetime.now(), "likes": 0
    }])
    df = pd.concat([df, new_post], ignore_index=True)
    df.to_csv(CSV_PATH, index=False, encoding='utf-8-sig')
    st.session_state.last_post_time = datetime.now()
    return True, "성공"

# 데이터 로드
df_posts = load_posts()

# ---------------------------------------------------------
# 3. 레이아웃
# ---------------------------------------------------------

# [대제목]
st.title("💬 전기인 자유게시판")

# [소개글]
st.markdown("""
현장의 땀방울부터 자격증 공부의 고충까지, 우리끼리 통하는 **무한 임피던스 소통 공간**입니다!  
뒷담화는 감전 주의 ⚡, 따뜻한 응원은 전력 전송 📈! 마음껏 전압을 높여보세요.  
*(단, 도배 시 차단기 내려갑니다. 😎)*
""")

st.divider()

main_col, side_col = st.columns([7, 3], gap="large")

# --- 게시글 렌더링 함수 ---
def render_post_item(row, key_prefix="main"):
    p_id = row['id']
    date_str = row['date'].strftime('%Y-%m-%d %H:%M')
    
    if st.session_state.get("edit_post_id") == p_id:
        with st.container(border=True):
            st.caption(f"✏️ 관리자 수정 모드")
            new_t = st.text_input("제목 수정", value=row['title'], key=f"edit_t_{p_id}")
            new_c = st.text_area("내용 수정", value=str(row['content']).replace("  \n", "\n"), key=f"edit_c_{p_id}")
            ec1, ec2 = st.columns([1, 5])
            if ec1.button("💾 저장", key=f"save_btn_{p_id}"):
                update_post_content(p_id, new_t, new_c)
                st.session_state.edit_post_id = None
                st.rerun()
            if ec2.button("❌ 취소", key=f"cancel_btn_{p_id}"):
                st.session_state.edit_post_id = None
                st.rerun()
    else:
        # [정렬] 제목 - 작성자 - 작성일 - 가압카운트수
        title_label = f"📝 {row['title']} | 👤 {row['author']} | 📅 {date_str} | ⚡ {row['likes']}"
        is_expanded = (st.session_state.expanded_post_id == p_id)
        
        with st.expander(title_label, expanded=is_expanded):
            st.markdown(f"<div style='line-height:1.1; margin-bottom:10px;'>{row['content']}</div>", unsafe_allow_html=True)
            
            is_admin = st.session_state.get("admin_logged_in", False)
            if is_admin:
                b_col1, b_col2, b_col3, b_col4 = st.columns([1, 1, 1, 7])
            else:
                b_col1, b_col2 = st.columns([1, 9])
            
            is_voted = p_id in st.session_state.voted_posts
            b_col1.button("⚡" if not is_voted else "✔️", key=f"{key_prefix}_like_{p_id}", disabled=is_voted, on_click=handle_like_callback, args=(p_id,), help="가압하기")
            
            if is_admin:
                if b_col2.button("✏️", key=f"edit_{p_id}", help="게시글 수정"):
                    st.session_state.edit_post_id = p_id
                    st.rerun()
                if b_col3.button("🗑️", key=f"del_{p_id}", help="게시글 삭제"):
                    delete_post(p_id)
                    st.toast("게시글이 삭제되었습니다.")
                    st.rerun()

# --- [좌측 메인 영역] ---
with main_col:
    # [1] 글쓰기 섹션
    with st.expander("✍️ 새로운 글 남기기", expanded=True):
        with st.form("write_form", clear_on_submit=True):
            f_author = st.text_input("닉네임", placeholder="익명")
            f_title = st.text_input("제목")
            f_content = st.text_area("내용")
            if st.form_submit_button("작성"):
                if f_title and f_content:
                    success, msg = save_post(f_author, f_title, f_content)
                    if success: st.rerun()
                    else: st.error(msg)

    # [2] 고정 위치: 안내 문구 및 서프라이즈 선물 문구
    st.markdown("### 📢 가압(공감) 버튼을 꾹 눌러주세요!") 
    st.success("💡 혹시 아나요? VoltMaster가 명예의 전당에 등극하신 분들께 짜릿한 **특고압 서프라이즈 선물**을 준비하고 있을지! 😎🎁")
    st.markdown("---")
    
    # [3] 게시글 목록
    st.markdown("### 📑 게시글 목록")
    if not df_posts.empty:
        sorted_posts = df_posts.sort_values(by='date', ascending=False)
        for _, row in sorted_posts.head(10).iterrows():
            render_post_item(row, key_prefix="main_list")
        
        if len(sorted_posts) > 10:
            with st.expander("➕ 이전 게시글 더보기"):
                for _, row in sorted_posts.iloc[10:].iterrows():
                    render_post_item(row, key_prefix="more_list")
    else:
        st.info("아직 게시글이 없습니다.")

# --- [우측 사이드 영역] ---
with side_col:
    st.subheader("🏆 명예의 전당")
    tab_w, tab_m, tab_y = st.tabs(["주간", "월간", "연간"])
    now = datetime.now()

    def render_fame(days):
        limit = now - timedelta(days=days)
        filtered = df_posts[(df_posts['date'] >= limit) & (df_posts['likes'] > 0)]
        if not filtered.empty:
            top_10 = filtered.sort_values(by='likes', ascending=False).head(10)
            for i, (_, r) in enumerate(top_10.iterrows()):
                crown = " 👑" if i == 0 else ""
                medal = "🥇" if i == 0 else "🥈" if i == 1 else "🥉" if i == 2 else "⚡"
                date_only = r['date'].strftime('%Y-%m-%d')
                st.markdown(f"{medal} **{r['title']}{crown}** (⚡{r['likes']}) <span style='color:gray; font-size:11px;'>[{date_only}]</span>", unsafe_allow_html=True)
        else:
            st.caption("집계된 글이 없습니다.")

    with tab_w: render_fame(7)
    with tab_m: render_fame(30)
    with tab_y: render_fame(365)

    st.divider()
    
    st.subheader("🆕 실시간 최신글")
    if not df_posts.empty:
        latest_side = df_posts.sort_values(by='date', ascending=False).head(10)
        for _, r in latest_side.iterrows():
            date_only = r['date'].strftime('%Y-%m-%d')
            st.markdown(f"• **{r['title']}** (⚡{r['likes']}) <span style='color:gray; font-size:11px;'>[{date_only}]</span>", unsafe_allow_html=True)

# 하단 카피라이트
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """<div style="text-align: center; opacity: 0.5; font-size: 11px; color: gray;">
    © 2026 VoltMaster. All rights reserved. 
    <a href="javascript:window.location.href='/?manage=true'" target="_self" style="color:rgba(0,0,0,0); font-size:10px; text-decoration:none; cursor:pointer;">.</a>
    </div>""", 
    unsafe_allow_html=True
)