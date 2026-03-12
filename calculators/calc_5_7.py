import streamlit as st
import pandas as pd

def run_calc():
    st.subheader("💨 5-7. 발전기 DPF 배압 및 재생 조건 분석")
    st.caption("비상발전기 DPF의 내부 압력(Back Pressure)을 진단하고 필터 재생을 위한 운전 조건을 판정합니다.")

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 발전기 운전 데이터")
        # 발전기 정격 대비 현재 부하
        gen_capacity = st.number_input("발전기 정격 용량 (kW)", value=2500, step=100)
        current_load = st.slider("현재 운전 부하 (kW)", 0, gen_capacity, int(gen_capacity * 0.8))
        
        # DPF 실시간 계측 데이터
        dpf_pressure = st.number_input("DPF 내부 배압 (mBar)", value=55.0, step=1.0, help="80mBar 초과 시 보통 Bypass 발생")
        exhaust_temp = st.number_input("배기 가스 온도 (℃)", value=280, step=10, help="재생을 위해서는 통상 300℃ 이상 필요")
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. DPF 시스템 설정치")
        c1, c2 = st.columns(2)
        limit_bypass = c1.number_input("Bypass 임계압력", value=80, step=5)
        limit_regen = c2.number_input("재생 시작압력", value=60, step=5)
        temp_regen = st.number_input("재생 요구온도 (℃)", value=300, step=10)

        btn = st.button("DPF 상태 정밀 진단 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 DPF 건전성 및 재생 판정")
        if btn:
            # --- 판정 로직 ---
            # 1. Bypass 및 위험 상태 판정
            if dpf_pressure >= limit_bypass:
                status = "🚨 Bypass 동작 (위험)"
                color = "red"
            elif dpf_pressure >= (limit_bypass * 0.85):
                status = "⚠️ 주의 (Bypass 임박)"
                color = "orange"
            else:
                status = "✅ 정상 운용 중"
                color = "green"
            
            # 2. 재생 조건 충족 여부 (압력 & 온도)
            press_ok = dpf_pressure >= limit_regen
            temp_ok = exhaust_temp >= temp_regen
            
            if press_ok and temp_ok:
                regen_decision = "💡 재생 실시 권장 (실부하 가동)"
            elif press_ok and not temp_ok:
                regen_decision = "🌡️ 온도 부족 (부하율 증대 필요)"
            elif not press_ok and temp_ok:
                regen_decision = "✨ 필터 청정 (재생 불필요)"
            else:
                regen_decision = "💤 대기 상태 (조건 미달)"

            # --- 결과 데이터프레임 (인덱스 제거) ---
            diag_items = [
                {"항목": "현재 배압 상태", "수치": f"{dpf_pressure} mBar", "판정": status},
                {"항목": "배기 온도 상태", "수치": f"{exhaust_temp} ℃", "판정": "조건 충족" if temp_ok else "온도 낮음"},
                {"항목": "필터 재생 가능성", "수치": "분석 완료", "판정": regen_decision}
            ]
            
            st.dataframe(pd.DataFrame(diag_items), hide_index=True, use_container_width=True)

            # --- 종합 지표 ---
            st.metric("배압 여유도 (Bypass 대비)", f"{limit_bypass - dpf_pressure:.1f} mBar")

            st.markdown("---")
            st.markdown("##### 💡 전문가 운영 가이드")
            st.info(f"""
            1. **배압 관리:** DPF 내부 필터 스택(Filter Stack)에 분진이 쌓이면 배압이 상승합니다. **{limit_bypass}mBar** 도달 시 엔진 보호를 위해 Bypass 댐퍼가 열리며 매연이 직배출됩니다.
            2. **필터 재생:** 압력이 **{limit_regen}mBar** 이상이고 배기 온도가 **{temp_regen}℃**를 상회할 때, 실부하 운전을 통해 1시간 이상 가동하면 내부 찌꺼기를 태워 재생할 수 있습니다.
            3. **부하 운전:** 현재 부하({current_load}kW)에서 온도가 낮다면, 단계적으로 부하를 높여 재생 온도를 확보하는 시나리오를 검토하십시오.
            """)
            
            
        else:
            st.info("발전기 운전 데이터를 입력하여 DPF의 매연 저감 성능 및 재생 주기를 시뮬레이션하십시오.")