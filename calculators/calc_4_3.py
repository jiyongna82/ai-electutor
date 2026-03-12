import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 4-3. 변압기 돌입전류(Inrush) 및 OCR 오동작 검토")
    st.caption("변압기 투입 시 발생하는 자속 포화 돌입전류를 추정하고, 보호계전기(OCR) 정정치와의 보호협조 적정성을 분석합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 변압기 및 투입 조건")
        tr_kva = st.number_input("변압기 정격 용량 (kVA)", min_value=10, value=1000, step=100)
        v_sys = st.selectbox("전압 등급 (V)", [380, 3300, 6600, 22900], index=3)
        
        # 돌입전류 배수 (정격전류 대비)
        inrush_multiplier = st.slider("돌입전류 배수 (정격 대비)", 5, 15, 10, 1, 
                                    help="일반적으로 유입식은 10~12배, 몰드식은 8~10배 수준입니다.")
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. 보호계전기(OCR) 설정값")
        ct_primary = st.number_input("CT 1차 정격 (A)", min_value=1, value=40, step=5)
        ct_ratio = ct_primary / 5
        
        # 순시(Instantaneous) 요소 설정
        inst_tap = st.number_input("OCR 순시(Instantaneous) 정정 (A)", min_value=10.0, value=40.0, step=5.0,
                                 help="계전기 2차측 입력 전류 기준 순시 동작값입니다.")

        btn = st.button("돌입전류 보호협조 분석 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 분석 및 판정 결과")
        if btn:
            # 1. 정격 전류 (In) 및 돌입전류 (I_inrush) 산출
            i_rated = tr_kva / (math.sqrt(3) * (v_sys / 1000))
            i_inrush_primary = i_rated * inrush_multiplier
            
            # 2. 계전기 유입 전류 산출 (CT 2차측 환산)
            i_inrush_secondary = i_inrush_primary / ct_ratio
            
            # 3. 오동작 여부 판정 (순시 요소와 비교)
            # 안전율 1.25배 적용 권장
            is_trip_risk = i_inrush_secondary >= inst_tap
            safety_margin = inst_tap / i_inrush_secondary if i_inrush_secondary > 0 else 0

            # --- 결과 시각화 ---
            if is_trip_risk:
                st.error(f"❌ **순시 오동작 위험:** 돌입전류({i_inrush_secondary:.2f}A)가 순시 정정치({inst_tap}A)를 초과합니다.")
            elif safety_margin < 1.25:
                st.warning(f"⚠️ **여유율 부족:** 협조는 가능하나 여유율({safety_margin:.2f})이 낮아 오동작 가능성이 있습니다.")
            else:
                st.success(f"✅ **보호협조 양호:** 여유율 {safety_margin:.2f}배로 안정적인 투입이 예상됩니다.")
                
            res_c1, res_c2 = st.columns(2)
            res_c1.metric("돌입전류 (1차측)", f"{i_inrush_primary:.1f} A")
            res_c2.metric("계전기 유입전류", f"{i_inrush_secondary:.1f} A")
            
            st.write(f"- 변압기 정격 전류: **{i_rated:.2f} A**")
            st.write(f"- 추천 순시 정정 범위: **{(i_inrush_secondary * 1.25):.1f} A 이상**")

            st.markdown("---")
            st.markdown("##### 💡 전문가 기술 가이드")
            st.info(f"""
            1. **돌입전류(Magnetizing Inrush):** 변압기 투입 시 철심의 잔류 자속에 의해 발생하는 과도 전류입니다. 초기 피크치는 정격의 **{inrush_multiplier}배**에 달하며 약 0.1초 이내에 감쇄합니다.
            2. **오동작 방지:** 순시 요소 정정 시 돌입전류 피크값에 대해 **25~50%의 여유**를 두는 것이 실무 관례입니다.
            3. **디지털 계전기 특성:** 최신 계전기는 **제2고조파 억제(Harmonic Restraint)** 기능을 통해 돌입전류와 사고전류를 구분하지만, 순시(Instantaneous) 요소는 고조파 억제 없이 동작하는 경우가 많으므로 주의가 필요합니다.
            """)
            
            st.latex(r"I_{inrush(sec)} = \frac{I_{rated} \times Multiplier}{CT_{ratio}}")
            st.latex(r"I_{inst} \geq I_{inrush(sec)} \times 1.25 \sim 1.5")
            
            
        else:
            st.info("변압기 사양과 계전기 설정값을 입력하여 투입 시 시뮬레이션을 진행하십시오.")