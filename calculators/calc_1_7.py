import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-7. 지중 케이블 허용전류 보정계수 및 실부하 분석")
    st.caption("지중 매설 환경(토양 온도, 매설 깊이, 인접 회로 수)에 따른 허용전류 보정계수를 산출하고, 실제 운전 가능한 허용전류(Iz)를 도출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 케이블 기본 제원")
        cable_type = st.selectbox("케이블 종류", ["0.6/1kV F-CV (XLPE)", "22.9kV FR-CNCO-W", "기타 고압 XLPE 케이블"], index=0)
        
        wire_sq = st.select_slider(
            "전선 굵기 (SQ)",
            options=[25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630],
            value=95
        )
        
        # 기본 허용전류 (지중 매설 기준 온도 20℃ 기준 예시 데이터)
        base_amp_map = {95: 260.0, 120: 300.0, 150: 340.0, 185: 390.0, 240: 460.0}
        base_amp = base_amp_map.get(wire_sq, 200.0)

        st.markdown("---")
        st.markdown("#### 🌡️ 2. 매설 환경 보정 조건")
        
        # 1. 주위 온도(토양) 보정 (기준 20℃)
        soil_temp = st.slider("주위 토양 온도 (℃)", 10, 40, 20, 5, help="토양 온도가 기준(20℃)보다 높으면 허용전류가 감소합니다.")
        
        # 2. 매설 깊이 보정 (기준 1.2m)
        burial_depth = st.selectbox("매설 깊이 (m)", [0.6, 0.8, 1.0, 1.2, 1.5, 2.0], index=3)
        
        # 3. 인접 회로 수 보정 (복수 회로 열 간섭)
        circuit_count = st.number_input("동일 경로 내 인접 회로 수", min_value=1, max_value=12, value=1)

        btn = st.button("지중 환경 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 보정 결과")
        if btn:
            # --- 보정 계수 산출 로직 ---
            # 1. 온도 보정계수 (f1) : XLPE 90℃ 운전 기준
            f1 = math.sqrt((90 - soil_temp) / (90 - 20))
            
            # 2. 매설 깊이 보정계수 (f2) : 표준 깊이 1.2m 기준
            depth_map = {0.6: 1.05, 0.8: 1.03, 1.0: 1.01, 1.2: 1.0, 1.5: 0.98, 2.0: 0.95}
            f2 = depth_map.get(burial_depth, 1.0)
            
            # 3. 인접 회로 보정계수 (f3) : 복수 회로 열 간섭 반영
            if circuit_count == 1: f3 = 1.0
            elif circuit_count == 2: f3 = 0.85
            elif circuit_count == 3: f3 = 0.75
            elif circuit_count <= 6: f3 = 0.70
            else: f3 = 0.60
            
            # 최종 합성 보정계수 및 허용전류
            total_f = f1 * f2 * f3
            final_iz = base_amp * total_f

            # --- 결과 시각화 ---
            st.success(f"✅ 최종 합성 보정계수: **{total_f:.2f}**")
            
            c_res1, c_res2 = st.columns(2)
            c_res1.metric("기본 허용전류 (20℃)", f"{base_amp} A")
            c_res2.metric("보정 후 허용전류 (Iz)", f"{final_iz:.1f} A")
            
            st.markdown("##### 📏 세부 보정 데이터")
            st.write(f"- 토양 온도({soil_temp}℃) 보정: **{f1:.2f}**")
            st.write(f"- 매설 깊이({burial_depth}m) 보정: **{f2:.2f}**")
            st.write(f"- 회로 집합({circuit_count}회로) 보정: **{f3:.2f}**")

            st.markdown("---")
            st.markdown("##### 💡 전문가 시공 가이드")
            st.info(f"""
            1. **방열 조건:** 지중은 공기 중 배선과 달리 토양의 열저항에 의해 냉각 성능이 제한됩니다. 주위 온도가 상습적으로 높은 지역이나 공장 지대는 보수적인 온도 설정을 권장합니다.
            2. **열 간섭 리스크:** 복수 회로를 동일 관로나 관대(Duct Bank)에 포설할 경우, 상호 열 간섭으로 인해 허용전류가 **최대 40% 이상 감소**할 수 있으므로 설계 시 반드시 반영해야 합니다.
            3. **매설 깊이 선정:** 깊게 매설할수록 외부 하중(중차량 등)에는 유리하지만, 지표면과의 방열 거리가 멀어져 허용전류 측면에서는 불리해집니다. KEC 매설 기준과 허용전류 사이의 균형을 맞추십시오.
            """)
            
            st.latex(r"I_z = I_0 \times f_{temp} \times f_{depth} \times f_{group}")
            
            
        else:
            st.info("좌측에 케이블 사양과 지중 매설 환경을 입력해 주세요.")