import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-2. 전압강하 산출 및 적정 전선 굵기(SQ) 선정")
    st.caption("배전 선로의 전압강하를 산출하고, KEC 규정 기준을 만족하는 최적의 전선 굵기를 자동으로 추천합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 선로 및 부하 조건")
        
        # 계통 전압 및 상식 선택
        system_type = st.selectbox("계통 방식", ["3상 4선식 (380V/220V)", "3상 3선식 (380V)", "단상 2선식 (220V)"], index=0)
        
        # 부하 데이터 입력
        load_p = st.number_input("부하 용량 (kW)", min_value=0.1, value=50.0, step=1.0)
        pf = st.slider("부하 역률 (%)", 70, 100, 90, 1) / 100.0
        
        # 선로 길이 입력
        length = st.number_input("선로 길이 (m)", min_value=1.0, value=100.0, step=10.0)
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 설계 및 규정 기준")
        
        # KEC 전압강하 허용 기준 (저압 수전 기준)
        limit_pct = st.select_slider(
            "허용 전압강하율 (%)",
            options=[3.0, 5.0, 6.0, 7.0, 8.0],
            value=5.0,
            help="KEC 기준: 조명(3%), 기타(5%) / 저압수전 100m 초과 시 추가 허용 가능"
        )
        
        conductor_material = st.radio("도체 재질", ["구리 (Copper)", "알루미늄 (Aluminum)"], horizontal=True)

        btn = st.button("전압강하 및 굵기 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 추천 결과")
        if btn:
            # 1. 계산 전압 설정
            v_ref = 380.0 if "3상" in system_type else 220.0
            
            # 2. 부하 전류 (I) 계산
            if "3상" in system_type:
                i_load = (load_p * 1000) / (math.sqrt(3) * v_ref * pf)
            else:
                i_load = (load_p * 1000) / (v_ref * pf)
            
            # 3. 전선 굵기별 전압강하 시뮬레이션 (구리 기준 고유저항 1/58 적용)
            rho = 1/58 if conductor_material == "구리 (Copper)" else 1/35
            SQ_LIST = [2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300]
            
            recommended_sq = SQ_LIST[-1]
            final_drop_v = 0.0
            final_drop_pct = 0.0
            
            for sq in SQ_LIST:
                # KEC 간이 계산식 적용 (e = K * I * L / (1000 * A))
                # K: 3상4선식(17.8), 3상3선식(30.8), 단상2선식(35.6)
                if "3상 4선식" in system_type: k_factor = 17.8
                elif "3상 3선식" in system_type: k_factor = 30.8
                else: k_factor = 35.6
                
                drop_v = (k_factor * i_load * length) / (1000 * sq)
                drop_pct = (drop_v / v_ref) * 100
                
                if drop_pct <= limit_pct:
                    recommended_sq = sq
                    final_drop_v = drop_v
                    final_drop_pct = drop_pct
                    break

            # --- 결과 시각화 ---
            st.success(f"✅ 권장 전선 굵기: **{recommended_sq} SQ**")
            
            st.markdown("##### 📏 상세 산출 데이터")
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("부하 전류 (In)", f"{i_load:.1f} A")
            res_c2.metric("전압 강하율", f"{final_drop_pct:.2f} %")
            
            st.write(f"- 계산된 전압강하: **{final_drop_v:.2f} V**")
            st.write(f"- 적용 도체: **{conductor_material}**")
            
            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **KEC 규정 준수:** 조명 부하는 **3%**, 기타 부하는 **5%** 이하 유지를 권장합니다. (저압수전 기준)
            2. **장거리 배선:** 선로 길이가 100m를 초과할 경우, 미터당 0.005%를 가산할 수 있으나 최대 **8%**를 넘지 않는 것이 안전합니다.
            3. **데이터센터 유의사항:** UPS 하단부 등 정밀 기기가 연결된 선로는 전압 품질을 위해 전압강하를 **2% 이내**로 설계하는 것이 실무적으로 유리합니다.
            """)
            
            # 수식 표시
            st.latex(r"e = \frac{K \cdot I \cdot L}{1000 \cdot A} \quad [V]")
            st.latex(r"Voltage \ Drop \ (\%) = \frac{e}{V_{ref}} \times 100")
        else:
            st.info("좌측에 부하 및 선로 조건을 입력한 후 분석 버튼을 눌러주세요.")