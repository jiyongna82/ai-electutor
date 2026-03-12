import streamlit as st
import math

def run_calc():
    st.subheader("📏 2-9. 배전반 모선(Busbar) 규격 및 허용전류 산출")
    st.caption("구리 부스바(Copper Busbar)의 규격별 허용전류를 산출하고, 단락 사고 시 발생하는 전자력에 대한 기계적 강도를 검토합니다.")

    # --- 부스바 허용전류 DB (표준 주위온도 40℃, 허용온도 65℃ 기준 대략치) ---
    # 규격: [폭(mm), 두께(mm), 허용전류(A)]
    BUSBAR_DB = [
        [20, 3, 210], [25, 3, 260], [30, 3, 310],
        [30, 5, 450], [40, 5, 580], [50, 5, 710], [60, 5, 840],
        [50, 10, 1100], [60, 10, 1300], [80, 10, 1650], [100, 10, 2000], [125, 10, 2400], [150, 10, 2800], [200, 10, 3600]
    ]

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 부하 조건 및 모선 선정")
        target_current = st.number_input("목표 정격 전류 (A)", min_value=10.0, value=1250.0, step=100.0)
        
        # 병렬 모선 수 (매수)
        num_bars = st.selectbox("모선 수량 (매/Phase)", [1, 2, 3, 4], index=0)
        
        # 규격 추천 및 선택
        recommended_idx = next((i for i, b in enumerate(BUSBAR_DB) if b[2] * num_bars >= target_current), len(BUSBAR_DB)-1)
        selected_spec = st.selectbox(
            "부스바 규격 선택 (폭 x 두께)", 
            options=[f"{b[0]} x {b[1]}" for b in BUSBAR_DB],
            index=recommended_idx
        )
        width, thick = map(int, selected_spec.split(' x '))

        st.markdown("---")
        st.markdown("#### ⚙️ 2. 환경 및 설치 조건")
        ambient_temp = st.slider("주위 온도 (℃)", 20, 60, 40, 5)
        
        # 단락 사고 조건
        st.markdown("#### ⚡ 3. 기계적 강도(단락) 검토 조건")
        i_sc_ka = st.number_input("예상 단락 전류 (kA)", min_value=1.0, value=25.0, step=5.0)
        bus_dist = st.number_input("상간 이격 거리 (mm)", min_value=50, value=150, step=10)
        support_len = st.number_input("지지물(애자) 간격 (mm)", min_value=100, value=500, step=50)

        btn = st.button("모선 규격 정밀 검증 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 부스바 설계 검증 결과")
        if btn:
            # --- [1] 온도 보정 허용전류 계산 ---
            # 보정계수 K = sqrt((허용온도 - 실제주위온도) / (허용온도 - 표준주위온도))
            # 기준: 허용 65, 표준 40
            k_temp = math.sqrt((65 - ambient_temp) / (65 - 40)) if ambient_temp < 65 else 0
            
            base_amp = next(b[2] for b in BUSBAR_DB if b[0] == width and b[1] == thick)
            # 복수 매수 적용 시 감소 계수 적용 (통상 2매: 1.6~1.8배, 3매: 2.0~2.2배)
            parallel_factor = 1.0 if num_bars == 1 else (1.7 if num_bars == 2 else 2.1)
            final_amp = base_amp * parallel_factor * k_temp

            # --- [2] 단락 시 전자력 계산 (F) ---
            # F = 2.04 * Is^2 * (L / d) * 10^-2 [kgf]
            force = (2.04 * (i_sc_ka**2) * (support_len / bus_dist)) * 0.1
            
            # --- 결과 시각화 ---
            st.success(f"✅ 선정 규격: **Cu {width}x{thick}t x {num_bars}매**")
            
            st.markdown("##### 🌡️ 1. 열적 허용전류 검토")
            st.write(f"- 표준 허용전류: **{base_amp * parallel_factor:,.0f} A**")
            st.write(f"- 주위온도({ambient_temp}℃) 보정 계수: **{k_temp:.2f}**")
            st.metric("최종 허용전류", f"{final_amp:,.1f} A", delta=f"{final_amp - target_current:,.1f} A 여유")
            
            if final_amp < target_current:
                st.error("❌ **용량 부족:** 선정된 규격이 목표 전류를 감당할 수 없습니다. 매수를 늘리거나 폭을 넓히십시오.")

            st.markdown("---")
            st.markdown("##### 🏗️ 2. 기계적 강도(전자력) 검토")
            st.write(f"단락 전류 **{i_sc_ka} kA** 발생 시 상간에 작용하는 힘:")
            st.metric("예상 최대 전자력", f"{force:,.2f} kgf")
            
            st.info(f"""
            💡 **설계 조언:** 1. 계산된 전자력 **{force:,.1f} kgf**를 지지 애자가 견딜 수 있는지 확인하십시오.
            2. 전자력이 너무 크다면 지지물 간격({support_len}mm)을 좁히거나 상간 거리({bus_dist}mm)를 넓혀야 합니다.
            3. 대전류(2000A 이상)의 경우 표피 효과와 근접 효과로 인해 모선의 배치를 '드럼(Drum)' 형태나 'ㄷ'자 형태로 고려하십시오.
            """)
            
            st.latex(r"F = 2.04 \times I_s^2 \times \frac{L}{d} \times 10^{-8} \ [N] \ (\text{simplified})")
        else:
            st.info("좌측에 부하 전류와 설치 조건을 입력하여 모선 규격을 검증하세요.")