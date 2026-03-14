import streamlit as st
import pandas as pd  # 오류 수정: import pd -> import pandas as pd

def run_calc():
    st.subheader("🖥️ 6-5. 서버 랙(Rack) 전력 밀도 및 LOP 부하 관리")
    st.caption("랙별 전력 밀도와 LOP(Local Operation Panel)의 상평형을 분석하여 말단 전원 사고를 예방합니다.")

    # --- LOP(Local Operation Panel) 기술 개요 ---
    with st.expander("📘 LOP(Local Operation Panel) 기술 가이드", expanded=False):
        st.markdown("""
        **LOP(Local Operation Panel)**는 데이터센터 전력 공급 계통의 최말단에 위치하는 **현장 제어 분전반**입니다. (Like. PDU)
        
        * **최종 분배**: UPS로부터 공급된 전원(1차)을 각 서버 랙(Rack)의 rPDU(2차 분기, 서버랙에 세로로 길게 설치되는 콘센트류)로 최종 분기합니다.
        * **상평형 관리**: R, S, T 각 상의 부하를 균등하게 배분하여 **중성선(N상) 전류 상승**과 **전압 불평형**을 억제합니다.
        * **보호 협조**: 상위 차단기와의 차단 특성을 고려하여 하위 랙 사고 시 해당 LOP 내에서 사고를 국소화(Selective Coordination)합니다.
        """)

    col1, col2 = st.columns([1, 1.2])

    with col1:
        st.markdown("#### 📥 1. 랙(Rack) 설계 및 계측")
        rack_id = st.text_input("분석 대상 랙 ID", value="R-01-01")
        design_capa = st.number_input("랙당 설계 전력 (kW/Rack)", value=6.6, step=1.1)
        
        st.markdown("---")
        st.markdown("#### 🔌 2. PDU 분기 부하 (220V)")
        c1, c2 = st.columns(2)
        pdu_a = c1.number_input("PDU A (A)", value=12.5, step=0.5)
        pdu_b = c2.number_input("PDU B (A)", value=11.8, step=0.5)
        
        st.markdown("---")
        st.markdown("#### ⚖️ 3. 상위 LOP 메인 부하")
        l1, l2, l3 = st.columns(3)
        lop_r = l1.number_input("R상 (A)", value=45.0)
        lop_s = l2.number_input("S상 (A)", value=42.0)
        lop_t = l3.number_input("T상 (A)", value=38.0)

        btn = st.button("정밀 진단 실행 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown(f"#### 🔍 {rack_id} 랙 및 LOP 진단 리포트")
        if btn:
            # --- 계산 로직 ---
            pwr_total = (220 * (pdu_a + pdu_b)) / 1000
            density_rate = (pwr_total / design_capa) * 100
            
            lop_list = [lop_r, lop_s, lop_t]
            lop_avg = sum(lop_list) / 3
            # 상불평형률 계산: (최대편차/평균) * 100
            unbalance_rate = (max([abs(x - lop_avg) for x in lop_list]) / lop_avg) * 100

            # --- 판정 로직 ---
            d_status = "🚨 위험" if density_rate > 90 else "⚠️ 주의" if density_rate > 70 else "✅ 정상"
            u_status = "⚠️ 불평형" if unbalance_rate > 15 else "✅ 평형"

            # 데이터프레임 구성 (열 너비 고정 및 정렬)
            res_data = {
                "분석 지표": ["랙 실시간 전력", "설계 대비 부하율", "LOP 상불평형률", "PDU A/B 편차"],
                "계측 데이터": [f"{pwr_total:.2f} kW", f"{density_rate:.1f} %", f"{unbalance_rate:.1f} %", f"{abs(pdu_a - pdu_b):.1f} A"],
                "진단 결과": [d_status, "운용 분석", u_status, "정상"]
            }
            
            st.dataframe(
                pd.DataFrame(res_data),
                use_container_width=True,
                hide_index=True,
                column_config={
                    "분석 지표": st.column_config.TextColumn("분석 지표", width="medium"),
                    "계측 데이터": st.column_config.TextColumn("계측 데이터", width="small"),
                    "진단 결과": st.column_config.TextColumn("진단 결과", width="small")
                }
            )

            st.metric("랙 전력 밀도", f"{density_rate:.1f} %", delta=f"{pwr_total - design_capa:.2f} kW")

            st.markdown("---")
            st.markdown("##### 💡 전문가 운영 인사이트")
            
            if unbalance_rate > 15:
                st.warning(f"**[상평형 경고]** 현재 LOP 상불평형률이 {unbalance_rate:.1f}%로 관리 기준(15%)을 초과했습니다. 이는 중성선 과열 및 불필요한 전력 손실의 원인이 됩니다.")

            st.info(f"""
            1. **LOP 관리 최적화**: LOP는 서버실 내부 가용성의 핵심입니다. 상불평형률을 낮추기 위해 단상 부하(Rack)를 타 상으로 재분배하는 작업을 검토하십시오.
            2. **밀도 및 냉방**: 현재 {pwr_total:.2f}kW의 전력 밀도는 설계 범위 내에 있으나, 70% 초과 시 국소 Hotspot 발생 가능성이 높아지므로 주의가 필요합니다.
            """)
            
            
        else:
            st.info("데이터를 입력하고 '정밀 진단 실행' 버튼을 클릭하십시오.")