import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 2-2. 변압기 %Z 및 단락전류 산출")
    st.caption("변압기의 퍼센트 임피던스(%Z)를 바탕으로 단락 사고 시 발생하는 최대 단락전류를 계산하여 보호계전 및 차단기 정격 선정의 근거를 제공합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 변압기 및 계통 제원")
        
        # 2-1, 2-3과 통일된 표준 정격 슬라이더 적용
        tr_kva = st.select_slider(
            "변압기 정격 용량 (kVA)",
            options=[100, 200, 300, 400, 500, 600, 750, 1000, 1250, 1500, 2000, 2500, 3000, 3500, 4000, 4500, 5000, 6000, 7000, 7500, 8000, 9000, 10000],
            value=1000
        )
        
        v_sec = st.selectbox("2차측 정격 전압 (V)", [220, 380, 440, 3300, 6600], index=1)
        
        # 임피던스 입력 (표준치 가이드 제공)
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 임피던스 설정")
        tr_z = st.number_input("변압기 %Z (Percent Impedance)", min_value=1.0, max_value=20.0, value=6.0, step=0.1, help="변압기 명판상의 %Z 값을 입력하세요. 보통 6% 내외입니다.")
        
        source_z_inc = st.checkbox("한전(전원측) 임피던스 포함", value=False)
        source_mva = 500.0
        if source_z_inc:
            source_mva = st.number_input("전원측 단락 용량 (MVA)", value=500.0, step=50.0)

        btn = st.button("단락 전류 정밀 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 단락 특성 분석 결과")
        if btn:
            # 1. 정격 전류 (In) 계산
            i_n = (tr_kva * 1000) / (math.sqrt(3) * v_sec)
            
            # 2. 합성 임피던스 계산
            total_z = tr_z
            if source_z_inc:
                # %Z_s = (Tr_MVA / Source_MVA) * 100
                source_z = ((tr_kva / 1000) / source_mva) * 100
                total_z += source_z
            
            # 3. 단락 전류 (Is) 계산
            i_s = (i_n * (100 / total_z))
            i_s_ka = i_s / 1000.0
            
            # 4. 단락 용량 (Ps) 계산
            p_s_mva = (math.sqrt(3) * v_sec * i_s) / 1000000.0

            # --- 결과 시각화 ---
            st.success(f"✅ 최대 단락 전류: **{i_s_ka:.2f} kA**")
            
            st.markdown("##### 📏 상세 산출 내역")
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("2차 정격 전류 (In)", f"{i_n:.1f} A")
            res_c2.metric("합성 %Z", f"{total_z:.2f} %")
            
            st.write(f"- 계산된 단락 용량: **{p_s_mva:.2f} MVA**")
            st.write(f"- 차단기 권장 차단 용량: **{math.ceil(i_s_ka * 1.2)} kA 이상** (20% 여유 권장)")
            
            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **%Z의 의미:** 변압기 2차측을 단락시키고 1차측에 전압을 인가하여 2차에 정격전류가 흐를 때의 전압 강하 비율입니다. 이 값이 작을수록 전압 변동률은 좋으나 단락 전류는 커집니다.
            2. **차단기 선정:** 산출된 **{i_s_ka:.2f}kA**는 대칭분 단락전류입니다. 차단기의 정격차단전류(ICs)는 이 값보다 큰 표준 규격(예: 12.5, 25, 40, 50kA 등)을 선정해야 합니다.
            3. **데이터센터 유의점:** 메인 변압기 직하단 ACB나 VCB는 가혹한 단락 고장에 노출되므로, 전원측 임피던스를 포함한 보수적인 계산이 필요합니다.
            """)
            
            # 수식 표시
            st.latex(r"I_n = \frac{P_{Tr}}{\sqrt{3} \times V}")
            st.latex(r"I_s = \frac{100}{\%Z} \times I_n")
            
            
        else:
            st.info("좌측에 변압기 사양을 입력한 후 분석 버튼을 눌러주세요.")