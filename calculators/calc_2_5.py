import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 2-5. CT(변류기) 정격 및 부담(Burden) 선정")
    st.caption("부하 용량에 따른 CT 비(Ratio) 선정과 연결 케이블/계측기 임피던스를 고려한 부담(VA) 적정성을 검증합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. CT 1차측 정격 선정")
        # 적용 설비 선택
        equipment = st.radio("적용 대상", ["수전 변압기", "비상 발전기", "일반 동력 부하"], horizontal=True)
        
        c1, c2 = st.columns(2)
        v_sys = c1.selectbox("계통 전압 (V)", [380, 440, 3300, 6600, 22900], index=4)
        cap_kva = c2.number_input("설비 용량 (kVA)", min_value=10.0, value=1000.0, step=100.0)
        
        # 여유율 설정 (변압기 1.25~1.5 / 전동기 2.0~2.5 등)
        default_margin = 1.5 if equipment == "수전 변압기" else 1.25
        margin = st.slider("CT 선정 여유율 (K)", 1.0, 3.0, default_margin, 0.05)

        st.markdown("---")
        st.markdown("#### 🔌 2. CT 부담(Burden) 검증")
        st.info("💡 CT 2차측 선로가 길어지면 부담(VA) 초과로 오차가 발생합니다.")
        
        ct_va_rating = st.selectbox("CT 정격 부담 (VA)", [2.5, 5, 10, 15, 25, 40], index=2)
        
        c3, c4 = st.columns(2)
        wire_sq = c3.selectbox("2차측 전선 굵기 (SQ)", [2.5, 4, 6], index=0)
        wire_len = c4.number_input("CT ~ 계측기 거리 (m)", min_value=1.0, value=10.0, step=1.0, help="편도 거리 입력 (왕복 저항은 자동 계산)")
        
        instrument_va = st.number_input("연결 기기(계전기/미터) 소비 부담 (VA)", value=1.0, step=0.5)

        btn = st.button("CT 정격 및 부담 검증 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 CT 선정 및 검증 리포트")
        if btn:
            # --- [1] CT 비(Ratio) 선정 ---
            i_n = (cap_kva * 1000) / (math.sqrt(3) * v_sys)
            i_ct_target = i_n * margin
            
            # 표준 CT 1차 정격 리스트
            standard_ct = [5, 10, 15, 20, 30, 40, 50, 75, 100, 150, 200, 250, 300, 400, 500, 600, 750, 800, 1000, 1200, 1500, 2000, 2500, 3000, 4000]
            selected_ct_1 = next((ct for ct in standard_ct if ct >= i_ct_target), standard_ct[-1])
            
            # --- [2] 부담(Burden) 계산 ---
            # 전선 저항 (Cu 20℃ 기준, SQ당 약 0.018 Ω/m)
            # R = ρ * L / S (왕복이므로 2배)
            rho = 0.0178
            r_wire = (rho * wire_len * 2) / wire_sq
            
            # 전선 소비 부담 (VA = I^2 * R, CT 2차 정격 5A 가정)
            i_sec = 5.0
            wire_va = (i_sec ** 2) * r_wire
            
            total_burden_va = wire_va + instrument_va
            safety_factor = (total_burden_va / ct_va_rating) * 100

            # --- 결과 시각화 ---
            st.success(f"✅ CT 선정 결과: **{selected_ct_1} / 5 A**")
            
            st.markdown("##### 📏 1. 정격 전류 및 선정 근거")
            st.write(f"- 부하 정격 전류 ($I_n$): **{i_n:.2f} A**")
            st.write(f"- 계산치 ($I_n \times K$): **{i_ct_target:.2f} A**")
            st.write(f"- ➔ 선정된 CT Ratio: **{selected_ct_1} / 5**")
            
            st.markdown("---")
            st.markdown("##### ⚖️ 2. 부담(Burden) 적정성 검토")
            
            # 게이지 시각화 (부담 사용률)
            st.write(f"CT 정격 부담 대비 사용률: **{safety_factor:.1f}%**")
            color = "green" if safety_factor < 75 else "orange" if safety_factor < 100 else "red"
            st.markdown(f"""
                <div style="width:100%; background-color:#e0e0e0; border-radius:5px;">
                    <div style="width:{min(safety_factor, 100)}%; background-color:{color}; height:20px; border-radius:5px;"></div>
                </div>
            """, unsafe_allow_html=True)
            
            c_res1, c_res2 = st.columns(2)
            c_res1.write(f"선로 손실: **{wire_va:.2f} VA**")
            c_res2.write(f"기기 부담: **{instrument_va:.2f} VA**")
            st.write(f"➔ 총 합성 부담: **{total_burden_va:.2f} VA** (정격 {ct_va_rating}VA)")

            if safety_factor > 100:
                st.error("🚨 **부담 초과:** 전선 저항이나 기기 부담이 CT 정격 용량을 넘었습니다. 전선을 굵게(4SQ 이상) 변경하거나 CT 정격 VA를 높여야 합니다.")
            elif safety_factor > 80:
                st.warning("⚠️ **여유 부족:** 부담 사용률이 높습니다. 추후 계측기 추가 시 오차가 커질 수 있습니다.")
            else:
                st.success("✅ **안전:** 부담 용량이 충분하며 정밀한 계측이 가능합니다.")

            st.markdown("#### 💡 전문가 설계 팁")
            st.info("""
            1. **과전류 정수(n):** 보호용 CT라면 고장 전류 시 포화를 막기 위해 n > 10 또는 n > 20 인 제품을 확인하세요.
            2. **오차 계급:** 계측용은 0.5급 이상, 보호용은 5P10/10P20 등의 규격을 확인하십시오.
            3. **극성 확인:** CT 설치 시 K(P1)-L(P2) 방향과 2차측 k(s1)-l(s2) 극성이 바뀌면 역전력이 계측되거나 계전기가 오동작합니다.
            """)
        else:
            st.info("좌측에 부하 용량과 CT 2차측 배선 정보를 입력하세요.")