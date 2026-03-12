import streamlit as st
import math

def run_calc():
    st.subheader("🛡️ 2-8. 메인 차단기(VCB/ACB) 정격 및 차단 용량 선정")
    st.caption("변압기 또는 수전 용량을 바탕으로 메인 차단기의 정격 전류(A)와 단락 사고 시 견뎌야 하는 정격 차단 전류(kA)를 산출합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 계통 및 변압기 제원")
        v_sys = st.selectbox("계통 공칭 전압 (V)", [380, 440, 3300, 6600, 22900], index=4)
        
        # VCB(고압) 또는 ACB(저압) 자동 판별
        cb_type = "VCB (진공차단기)" if v_sys >= 3300 else "ACB (기중차단기)"
        st.info(f"선택된 전압 기준 적용 차단기: **{cb_type}**")

        tr_kva = st.number_input("변압기 정격 용량 (kVA)", min_value=10.0, value=1000.0, step=100.0)
        tr_z = st.number_input("변압기 퍼센트 임피던스 (%Z)", min_value=1.0, value=6.0, step=0.1)

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 선정 여유율 및 조건")
        af_margin = st.slider("정격 전류 여유율 (%)", 100, 200, 125, 5, help="부하의 연속운전 및 증설을 고려한 여유치 (통상 1.25~1.5배)")
        
        # 전원측 임피던스 고려 여부
        source_z_include = st.checkbox("한전(전원측) 임피던스 포함 계산", value=False)
        source_mva = 500.0
        if source_z_include:
            source_mva = st.number_input("전원측 단락 용량 (MVA)", value=500.0, step=50.0)

        btn = st.button("차단기 정격 상세 산출 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 차단기 선정 가이드라인")
        if btn:
            # --- [1] 정격 전류(In) 산출 ---
            i_n = (tr_kva * 1000) / (math.sqrt(3) * v_sys)
            i_af_target = i_n * (af_margin / 100.0)
            
            # --- [2] 단락 전류(Is) 산출 ---
            # %Z 환산
            total_z = tr_z
            if source_z_include:
                # 전원측 %Z = (TR_MVA / Source_MVA) * 100
                source_z = ((tr_kva / 1000) / source_mva) * 100
                total_z += source_z
            
            i_sc_ka = (i_n * (100 / total_z)) / 1000.0

            # --- [3] 표준 정격 매칭 ---
            # 표준 AF(Ampere Frame) 리스트
            standard_af = [400, 630, 800, 1000, 1250, 1600, 2000, 2500, 3200, 4000, 5000, 6300]
            selected_af = next((af for af in standard_af if af >= i_af_target), standard_af[-1])
            
            # 표준 kA(정격차단전류) 리스트
            standard_ka = [5, 8, 12.5, 20, 25, 31.5, 40, 50, 65, 85, 100]
            selected_ka = next((ka for ka in standard_ka if ka >= i_sc_ka), standard_ka[-1])

            # --- 결과 시각화 ---
            st.success(f"✅ 권장 사양: **{v_sys/1000 if v_sys>=1000 else v_sys}kV {selected_af}A {selected_ka}kA**")
            
            st.markdown("##### 📏 1. 정격 전류(Ampere Frame) 검토")
            st.write(f"- 부하 정격 전류 ($I_n$): **{i_n:.2f} A**")
            st.write(f"- 여유율 적용 목표치: **{i_af_target:.2f} A**")
            st.write(f"- ➔ 선정된 AF 규격: **{selected_af} AF**")
            
            st.markdown("---")
            st.markdown("##### ⚡ 2. 단락 용량(Interrupting Capacity) 검토")
            st.latex(r"I_s = \frac{100}{\%Z_{Total}} \times I_n")
            st.write(f"- 합성 퍼센트 임피던스: **{total_z:.3f} %**")
            st.write(f"- 계산된 단락 전류: **{i_sc_ka:.2f} kA**")
            st.write(f"- ➔ 선정된 정격 차단 전류: **<span style='color:red; font-size:1.1em;'>{selected_ka} kA</span>**", unsafe_allow_html=True)

            st.markdown("#### 💡 전문가 설계 코멘트")
            st.info(f"""
            1. **비대칭 계수 고려:** 고압 VCB의 경우 단락 시 비대칭 전류에 견디는 능력이 중요합니다. (KSC IEC 기준 확인)
            2. **AT(Ampere Trip) 설정:** {cb_type}의 트립 정격(AT)은 실제 부하 전류에 맞춰 정밀 정정하십시오.
            3. **선택 차단(Selectivity):** 상위 차단기(Main)와 하위 차단기(Branch) 간의 차단 시간 차이를 두어 사고 구간만 분리되도록 보호 협조를 검토하십시오.
            """)
            
        else:
            st.info("좌측에 변압기 용량과 %Z를 입력하여 차단기 정격을 확인하세요.")