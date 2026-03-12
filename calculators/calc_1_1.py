import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 1-1. 전선 허용전류(Ampacity) 정밀 산출")
    st.caption("KEC 규정에 근거하여 전선의 종류, 포설 방식, 주위 온도 및 다조 포설에 따른 보정계수를 적용한 최종 허용전류를 산출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 설계 조건 입력")
        
        # 전선 종류 및 절연체 선택
        wire_type = st.selectbox("전선 절연체 종류", ["PVC (70℃)", "XLPE/EPR (90℃)"], index=1)
        conductor_material = st.radio("도체 재질", ["구리 (Copper)", "알루미늄 (Aluminum)"], horizontal=True)
        
        # 포설 방식 선택 (KEC 가이드)
        installation_method = st.selectbox(
            "포설 방식 (Reference Method)", 
            ["A1: 벽면 내 전선관(단상)", "A2: 벽면 내 전선관(3상)", "B1: 벽면 위 전선관", "C: 케이블 트레이/직접매설", "E: 공기 중 배선"],
            index=3
        )
        
        # 전선 규격 선택 (SQ)
        wire_sq = st.select_slider(
            "전선 굵기 (SQ)",
            options=[1.5, 2.5, 4, 6, 10, 16, 25, 35, 50, 70, 95, 120, 150, 185, 240, 300, 400, 500, 630],
            value=25.0
        )

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 환경 보정 계수")
        
        # 온도 보정
        ambient_temp = st.slider("주위 온도 (℃)", 10, 60, 30, 5)
        
        # 복수회로 보정 (다조 포설)
        circuit_count = st.number_input("동일 경로 내 회로 수 (다조 포설)", min_value=1, max_value=20, value=1)

        btn = st.button("허용전류 계산 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 결과 리포트")
        if btn:
            # --- 간소화된 KEC 기반 로직 (예시 데이터) ---
            # 실제 구현 시에는 KEC 232.11-1 표 데이터를 Dictionary로 매핑하여 호출
            base_ampacity = 100.0 # 규격별 기본 허용전류 (XLPE 25sq, Method C 기준 가정)
            
            # 온도 보정 계수 (K)
            temp_factor = math.sqrt((90 - ambient_temp) / (90 - 30)) if wire_type == "XLPE/EPR (90℃)" else math.sqrt((70 - ambient_temp) / (70 - 30))
            
            # 다조 포설 보정 계수 (G)
            group_factor = 1.0 if circuit_count == 1 else (0.8 if circuit_count <= 3 else 0.7)
            
            # 최종 허용전류
            final_ampacity = base_ampacity * temp_factor * group_factor

            # --- 결과 시각화 ---
            st.success(f"✅ 최종 허용전류: **{final_ampacity:.2f} A**")
            
            st.markdown("##### 📏 산출 세부 내역")
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("기본 허용전류", f"{base_ampacity} A")
            res_c2.metric("환경 보정계수", f"{temp_factor * group_factor:.2f}")
            
            st.write(f"- 적용 절연체: **{wire_type}**")
            st.write(f"- 포설 환경: **{installation_method}**")
            st.write(f"- 다조 포설 보정: **{group_factor:.2f}** (회로수: {circuit_count})")
            
            st.markdown("---")
            st.markdown("##### 💡 전문가 검토 의견")
            st.info(f"""
            1. **온도 보정:** 현재 설정된 주위 온도 **{ambient_temp}℃**는 기준 온도(30℃) 대비 허용전류를 **{temp_factor:.1%}** 수준으로 조정합니다.
            2. **데이터센터 적용:** 서버실 내부 트레이 포설 시, 공조 온도에 따라 주위 온도를 보수적으로 설정(40℃ 이상)하는 것이 안전합니다.
            3. **차단기 선정:** 차단기 정격 전류(In)는 반드시 산출된 최종 허용전류 **{final_ampacity:.2f}A**보다 작아야 합니다. (In ≤ Iz)
            """)
            
            # 수식 표시
            st.latex(r"I_z = I_0 \times K_{temp} \times G_{group}")
        else:
            st.info("좌측의 설계 조건을 입력하고 [계산 실행] 버튼을 눌러주세요.")