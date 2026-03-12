import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("⚡ 1-3. 케이블 트레이 단면적 및 점적률(%) 계산")
    st.caption("케이블 트레이 내 포설되는 전선의 총 단면적을 산출하고, KEC 규정에 따른 허용 적재량(점적률) 준수 여부를 검토합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 트레이 규격 입력")
        t_width = st.number_input("트레이 폭 (mm)", min_value=100, value=600, step=50)
        t_height = st.number_input("트레이 높이 (mm)", min_value=40, value=100, step=10)
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 포설 케이블 구성")
        
        # 케이블 입력 테이블 형식 모사
        st.write("포설할 케이블의 외경과 수량을 입력하세요.")
        
        if 'cable_data' not in st.session_state:
            st.session_state.cable_data = [{"외경(mm)": 25.0, "수량(조)": 3}]

        def add_row():
            st.session_state.cable_data.append({"외경(mm)": 0.0, "수량(조)": 0})

        # 입력 인터페이스
        new_data = []
        for i, row in enumerate(st.session_state.cable_data):
            r1, r2 = st.columns(2)
            d = r1.number_input(f"케이블 {i+1} 외경 (mm)", value=row["외경(mm)"], key=f"d_{i}")
            n = r2.number_input(f"케이블 {i+1} 수량 (조)", value=row["수량(조)"], key=f"n_{i}")
            new_data.append({"외경(mm)": d, "수량(조)": n})
        st.session_state.cable_data = new_data

        st.button("➕ 케이블 종류 추가", on_click=add_row)
        
        limit_rate = st.slider("목표 제한 점적률 (%)", 20, 100, 50, 5, help="KEC 표준은 제어용 50%, 전력용은 단층 포설 등을 기준으로 합니다.")

        btn = st.button("점적률 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 트레이 점적률 분석 결과")
        if btn:
            # 1. 트레이 전체 단면적
            tray_area = t_width * t_height
            
            # 2. 케이블 총 단면적 계산
            total_cable_area = 0
            for row in st.session_state.cable_data:
                area = ( (row["외경(mm)"]**2) * 3.141592 / 4 ) * row["수량(조)"]
                total_cable_area += area
            
            # 3. 점적률 계산
            current_rate = (total_cable_area / tray_area) * 100
            
            # --- 결과 시각화 ---
            if current_rate <= limit_rate:
                st.success(f"✅ 분석 결과: **안전 (Pass)**")
            else:
                st.error(f"❌ 분석 결과: **설계 변경 필요 (Fail)**")
            
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("트레이 내부 면적", f"{tray_area:,.1f} mm²")
            res_c2.metric("현재 점적률", f"{current_rate:.2f} %")
            
            st.write(f"- 케이블 점유 면적: **{total_cable_area:,.1f} mm²**")
            st.write(f"- 허용 제한 점적률: **{limit_rate} %**")
            
            # 프로그레스 바 시각화
            st.progress(min(current_rate / 100, 1.0))

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **KEC 232.41 규정:** 다심 케이블의 경우 트레이 내측 단면적의 **50% 이하**로 포설하는 것을 원칙으로 합니다.
            2. **단층 포설(Single Layer):** 전력용 굵은 케이블은 발열 문제로 인해 점적률과 관계없이 **지름의 1.2배 간격**으로 단층 포설하는 것이 권장됩니다.
            3. **데이터센터 유의사항:** 통신 트레이와 전력 트레이는 분리 설치하며, 향후 서버 증설을 고려하여 초기 점적률은 **30~40%** 수준으로 여유 있게 설계하는 것이 실무적입니다.
            """)
            
            st.latex(r"Fill \ Ratio \ (\%) = \frac{\sum (\frac{\pi \cdot d_i^2}{4} \cdot n_i)}{W \cdot H} \times 100")
        else:
            st.info("좌측에 트레이 규격과 포설할 케이블 정보를 입력해 주세요.")