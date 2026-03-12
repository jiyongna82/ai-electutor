import streamlit as st
import math

def run_calc():
    st.subheader("⚡ 2-6. PT(계기용 변압기) 정격 및 퓨즈 선정")
    st.caption("계통 전압과 결선 방식에 따른 PT 비(Ratio)를 산출하고, 1차/2차 보호용 퓨즈의 정격을 추천합니다.")

    col1, col2 = st.columns([1, 1.2])
    
    with col1:
        st.markdown("#### 📥 1. 계통 및 결선 방식 설정")
        # 계통 전압 선택
        v_sys = st.selectbox("계통 공칭 전압 (V)", [220, 380, 440, 3300, 6600, 22900, 154000], index=5)
        
        # 결선 방식 (V-V는 2대, Y-Y는 3대 등 실무적 차이)
        pt_conn = st.radio("PT 결선 방식", ["V-V 결선 (2대 사용)", "Y-Y 결선 (3대 사용)", "가공선로 GPT (Open-Delta)"], horizontal=False)
        
        st.markdown("---")
        st.markdown("#### ⚙️ 2. PT 상세 사양")
        pt_va = st.selectbox("PT 정격 부담 (VA/대당)", [25, 50, 100, 200], index=1)
        pt_class = st.selectbox("오차 계급 (Accuracy Class)", ["0.5 (계측용)", "1.0 (일반)", "3.0 (보호용)"], index=0)
        
        st.markdown("---")
        st.markdown("#### 🛡️ 3. 퓨즈 선정 조건")
        f_margin = st.slider("퓨즈 선정 여유율 (%)", 100, 300, 150, 10, help="일반적으로 PT 정격전류의 1.5~2배 선정")

        btn = st.button("PT 및 퓨즈 정격 분석 🚀", type="primary", use_container_width=True)

    with col2:
        st.markdown("#### 🔍 PT 설계 및 보호 협조 리포트")
        if btn:
            # --- [1] PT 비(Ratio) 산출 ---
            # 2차 정격 전압은 표준 110V 고정
            v_sec_std = 110
            
            if "Y-Y" in pt_conn or "GPT" in pt_conn:
                # 상전압 기준 (V / √3)
                v_pri_pt = v_sys / math.sqrt(3)
                v_sec_pt = v_sec_std / math.sqrt(3)
                pt_ratio_text = f"({v_sys}/√3) / ({v_sec_std}/√3) [V]"
            else:
                # 선간전압 기준 (V-V 결선 등)
                v_pri_pt = v_sys
                v_sec_pt = v_sec_std
                pt_ratio_text = f"{v_sys} / {v_sec_std} [V]"

            pt_ratio = v_pri_pt / v_sec_pt

            # --- [2] 퓨즈(Fuse) 정격 산출 ---
            # 1차측 정격 전류 (I = VA / V)
            i_pri_nom = pt_va / v_pri_pt
            i_fuse_pri = i_pri_nom * (f_margin / 100.0)
            
            # 2차측 정격 전류
            i_sec_nom = pt_va / v_sec_pt
            i_fuse_sec = i_sec_nom * (f_margin / 100.0)

            # --- 결과 시각화 ---
            st.success(f"✅ PT Ratio 선정: **{pt_ratio_text}**")
            
            st.markdown("##### 📏 1. PT 전기적 특성")
            st.write(f"- 계산된 PT 비 (Nominal Ratio): **{pt_ratio:.2f}**")
            st.write(f"- 대당 정격 용량: **{pt_va} VA** (오차계급 {pt_class})")
            
            st.markdown("---")
            st.markdown("##### 🛡️ 2. 보호 퓨즈(Fuse) 추천 정격")
            
            c_f1, c_f2 = st.columns(2)
            with c_f1:
                st.write("**1차측 (High Side)**")
                st.write(f"정격 전류: {i_pri_nom*1000:.3f} mA")
                # 고압 퓨즈는 최소 단위가 있으므로 가이드 제공
                st.info(f"추천: **0.5A ~ 1.0A**\n(단락보호용 고압 전력퓨즈)")
                
            with c_f2:
                st.write("**2차측 (Low Side)**")
                st.write(f"정격 전류: {i_sec_nom:.3f} A")
                st.success(f"추천: **{max(1.0, math.ceil(i_fuse_sec))} A**\n(배선보호용 퓨즈/MCB)")

            st.markdown("#### 💡 전문가 기술 가이드")
            
            if "V-V" in pt_conn:
                st.info("💡 **V-V 결선 특성:** 2대의 PT로 3상 전압을 측정하며, 결선 시 극성(L1-L2, L2-L3)에 주의하십시오.")
            elif "Y-Y" in pt_conn:
                st.info("💡 **Y-Y 결선 특성:** 중성점 접지가 가능하며, 1차측 중성점은 이상전압 억제를 위해 직접 접지하거나 고저항 접지를 검토하십시오.")
            elif "GPT" in pt_conn:
                st.warning("⚠️ **GPT 유의사항:** 3차 권선(Open-Delta)은 지락 사고 시 영상 전압(OVGR) 검출용입니다. 제한 저항(CLR) 수치를 반드시 확인하십시오.")
                

            st.caption("※ 본 계산은 표준 규격 기준이며, 실제 제조사의 제작 사양 및 한전 수전 기준을 우선하여 적용하십시오.")
        else:
            st.info("좌측에서 계통 전압과 결선 방식을 선택하고 분석 버튼을 누르세요.")