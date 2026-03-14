import streamlit as st
from comments_tool import render_board  # 분리된 게시판 모듈 불러오기
import pandas as pd

# --- 수정된 카카오 공유 섹션 (기존 코드 구조 유지) ---
KAKAO_JS_KEY = "e9f5dad37078cba34364ca3f9acb4854"

def inject_share_buttons():
    st.markdown(f"""
        <script src="https://t1.kakaocdn.net/kakao_js_sdk/2.7.0/kakao.min.js"></script>
        <script>
            function initKakao() {{
                try {{
                    if (window.Kakao) {{
                        if (!Kakao.isInitialized()) {{
                            Kakao.init('{KAKAO_JS_KEY}');
                        }}
                    }}
                }} catch (e) {{ console.error(e); }}
            }}

            function shareKakao() {{
                initKakao();
                if (!Kakao.isInitialized()) {{
                    alert("카카오 SDK 초기화 실패. 플랫폼 설정을 확인해주세요.");
                    return;
                }}

                Kakao.Share.sendDefault({{
                    objectType: 'feed',
                    content: {{
                        title: '⚡ VoltMaster Insight: Vol. 05',
                        description: '2026 전력망의 대전환: AI 데이터센터와 차세대 에너지 솔루션',
                        imageUrl: 'https://cdn-icons-png.flaticon.com/512/2992/2992143.png',
                        link: {{
                            mobileWebUrl: window.location.href,
                            webUrl: window.location.href,
                        }},
                    }},
                    buttons: [
                        {{
                            title: '뉴스레터 읽기',
                            link: {{
                                mobileWebUrl: window.location.href,
                                webUrl: window.location.href,
                            }},
                        }},
                    ],
                }});
            }}
            setTimeout(initKakao, 500);
        </script>

        <style>
            .share-container-top {{
                position: fixed;
                top: 80px;
                right: 20px;
                z-index: 999;
                display: flex;
                flex-direction: column;
                gap: 10px;
            }}
            .share-btn {{
                width: 45px;
                height: 45px;
                border-radius: 50%;
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            }}
            .kakao {{ background-color: #FEE500; }}
        </style>

        <div class="share-container-top">
            <button class="share-btn kakao" onclick="shareKakao()">
                <img src="https://developers.kakao.com/assets/img/about/logos/kakaotalksharing/kakaotalk_sharing_btn_medium.png" width="25">
            </button>
        </div>
    """, unsafe_allow_html=True)

inject_share_buttons()

# --- 1. [Intro] 뉴스레터 헤더 & 오프닝 ---
st.markdown("""
# ⚡ VoltMaster Insight: Vol. 05
### **"데이터센터 전용 DCC 정격의 이해와 누전 메커니즘의 재발견"**
---
""")

st.info("""
**[Editor's Message]** 반갑습니다. 전력 계통의 안정과 혁신을 지향하는 **VoltMaster** 나지용입니다.  

변덕스러운 봄 날씨 속에 냉각탑 수위 제어와 비상발전기 히터 점검으로 현장은 분주하지만, 우리 센터의 '강철 심장'을 지킨다는 자부심으로 가득한 요즘입니다.  

이번 5호에서는 24시간 전력 질주하는 **DCC 발전기의 '강철 체력'** 이야기부터, 수도꼭지 비유로 아주 쉽게 풀어낸 **누전(지락) 메커니즘**, 그리고 놓치기 아까운 **상반기 주요 전시회** 소식을 담았습니다. 특히 고단한 일상 속 리프레시를 위한 **'전기인 성지 순례'** 코스까지 알차게 준비했으니, 이번 뉴스레터가 여러분의 기술적 갈증을 시원하게 해소해 드리는 단비가 되길 바랍니다.
""")

# --- 2. [Deep Dive] 비상발전기 정격(Rating)의 상세 이해 ---
st.markdown("## 📚 Deep Dive: 발전기의 '체력'과 설계 정격")
with st.container(border=True):
    st.markdown("### **Standby, Prime, DCC? 우리 현장에 맞는 엔진은?**")
    
    st.write("""
    비상발전기는 정전 시 얼마나 **'오래'**, **'강하게'** 버틸 수 있느냐에 따라 정격(Rating)이 결정됩니다. 
    이것을 우리 주변에서 흔히 볼 수 있는 이동 수단에 비유하면 이해가 훨씬 빠릅니다.

    * 🚗 **'시내 주행용' - Standby**: 
      가까운 거리를 잠깐 이동할 때 쓰는 승용차처럼, 정전 시 한전 전기가 들어올 때까지만 **단시간** 동안 버티는 용도입니다. 엔진을 최대치로 쓰기 때문에 오래 달리면 무리가 갑니다.
      
    * 🚛 **'장거리 화물용' - Prime**: 
      무거운 짐을 싣고 고속도로를 밤새 달리는 트럭처럼, 한전 전기가 없는 곳에서 **24시간 내내** 돌아가는 용도입니다. 다만, 엔진 보호를 위해 가끔은 가속 페달을 살짝 떼는(평균 부하율 70% 제한) 완급 조절이 필요합니다.
      
    * 🏎️ **'24시간 레이싱용' - DCC**: 
      한 번의 멈춤 없이 전력 질주하는 르망 24시 레이싱카처럼, **부하율 100%의 풀파워**로 1년 365일 내내 달릴 수 있도록 설계된 데이터센터 전용 엔진입니다. 서버의 일정한 부하를 견디는 '강철 체력'을 가졌습니다.
    """)

    # 1. 비교표 (와이드 출력)
    st.markdown("#### **[발전기 정격별 핵심 비교표]**")
    data = {
        "구분": ["Standby (ESP)", "Prime (PRP)", "DCC (Data Center)"],
        "엔진 비유": ["100m 단거리 질주", "완급조절 마라톤", "전력질주 마라톤"],
        "연간 운전 시간": ["최대 200~500시간", "시간 제한 없음", "시간 제한 없음"],
        "평균 부하율": ["70% 이하 유지 권장", "70% 수준 유지 권장", "100% 지속 운전 가능"],
        "과부하 능력": ["없음 (최대 출력 상태)", "10% 과부하 (12시간 중 1시간)", "제조사 협의 (일반적 없음)"],
        "주요 적용처": ["일반 빌딩, 아파트", "전력망 미비 지역, 공장", "데이터센터, 미션 크리티컬"]
    }
    df_rating = pd.DataFrame(data)
    st.dataframe(df_rating, use_container_width=True, hide_index=True)

    st.markdown("---")

    # 2. 1X3 구조의 상세 설명 배치
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🏃 Standby (ESP)")
        st.markdown("##### **'정전 시 잠깐 쓰는 보험'**")
        st.info("""
        - **용도:** 비상 시 긴급 전력 공급
        - **특징:** 엔진의 가용 한계치까지 출력을 높여 설계됩니다.
        - **주의:** 연간 가동 시간이 정해져 있어, 장시간 운전 시 엔진 소손 위험이 큽니다.
        """)

    with col2:
        st.subheader("🚴 Prime (PRP)")
        st.markdown("##### **'스스로 도는 주전원'**")
        st.info("""
        - **용도:** 상용 전원 대용 (오지, 건설현장)
        - **특징:** 무제한 가동이 가능하지만, 엔진 보호를 위해 70% 힘으로 달려야 합니다.
        - **장점:** 일시적인 10% 과부하를 견딜 여유가 있습니다.
        """)

    with col3:
        st.subheader("🏋️ DCC (Data Center)")
        st.markdown("##### **'지치지 않는 강철 엔진'**")
        st.success("""
        - **용도:** 데이터센터 서버 전용
        - **특징:** 24시간 내내 **100% 풀파워**로 가동해도 문제가 없는 등급입니다.
        - **배경:** 부하 변화가 거의 없는 서버 부하 특성에 완벽히 최적화되어 있습니다.
        """)

    st.markdown("<br>", unsafe_allow_html=True)
    

    # 3. 전문가 보강 팁
    with st.expander("🧐 전문가를 위한 심층 분석 (Expert Insights)", expanded=True):
        st.markdown("""
        **1. 정격별 출력 크기의 역설 (The Rating Paradox)**
        동일한 크기의 엔진이라도 정격에 따라 명시된 kW 수치는 다릅니다.
        * **출력 크기:** Standby(100%) > DCC(약 90%) > Prime(약 80%)
        * 더 오래, 더 꾸준히 일해야 하는 등급일수록 엔진의 안전 마진을 위해 용량을 보수적으로 책정합니다.

        **2. 데이터센터 설계와 Uptime Institute**
        Tier III 이상의 데이터센터 인증을 위해서는 가동 시간 제한이 있는 Standby 대신, **DCC 정격**이나 **Continuous 정격** 엔진을 선정하는 것이 표준입니다.

        **3. 저부하 운전의 위험성 (Wet Stacking)**
        DCC 등급이라 하더라도 정격의 30% 미만으로 오래 돌리면 불완전 연소로 배기 계통에 찌꺼기가 쌓입니다. 주기적인 실부하 테스트(Load Bank Test)가 필요한 이유입니다.
        """)

st.markdown("<br>", unsafe_allow_html=True)

# --- 3. [Hot Issue] 주요 전시회 & 박람회 정보 ---
st.markdown("## 📍 주요 전시회 & 박람회 정보")
st.caption("2026년 상반기, 전력 및 데이터센터 엔지니어를 위한 핵심 기술 이벤트 큐레이션")

col1, col2, col3 = st.columns(3)

# [박스 1: EPTK]
with col1:
    with st.container(border=True):
        head_col1, head_col2 = st.columns([1, 4])
        with head_col1: st.image("https://cdn-icons-png.flaticon.com/512/2992/2992143.png") 
        with head_col2: st.markdown("### **EPTK 2026**\n**국제 전기전력 전시회**")
        st.markdown("📅 **2026. 05. 06 ~ 05. 08**\n📍 **서울 COEX C홀**")
        img_url1 = "https://electrickorea.org/wp-content/uploads/2025/09/01_img01-2.jpg"
        st.markdown(f'<div style="width: 100%; height: 180px; overflow: hidden; border-radius: 8px; margin-bottom: 5px;"><img src="{img_url1}" style="width: 100%; height: 100%; object-fit: cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown("* 디지털 보호계전기(IED)\n* 부분방전(PD) 진단\n* KEC 대응 보호협조")
        st.link_button("상세 보기", "http://www.electrickorea.org/", use_container_width=True)

# [박스 2: HARFKO]
with col2:
    with st.container(border=True):
        head_col1, head_col2 = st.columns([1, 4])
        with head_col1: st.image("https://cdn-icons-png.flaticon.com/512/11100/11100067.png")
        with head_col2: st.markdown("### **HARFKO 2026**\n**한국국제냉난방공조전**")
        st.markdown("📅 **2026. 10. 21 ~ 10. 23**\n📍 **일산 KINTEX 제1장**")
        img_url2 = "https://www.harfko.com/file_upload/assets/img/exhibit_img/2022/2022_photo11.jpg"
        st.markdown(f'<div style="width: 100%; height: 180px; overflow: hidden; border-radius: 8px; margin-bottom: 5px;"><img src="{img_url2}" style="width: 100%; height: 100%; object-fit: cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown("* 무급유 터보냉동기\n* 액침냉각(DTC) 실증\n* 폐열 회수 시스템")
        st.link_button("상세 보기", "http://www.harfko.com/", use_container_width=True)

# [박스 3: 에너지대전]
with col3:
    with st.container(border=True):
        head_col1, head_col2 = st.columns([1, 4])
        with head_col1: st.image("https://cdn-icons-png.flaticon.com/512/427/427735.png")
        with head_col2: st.markdown("### **2026 대한민국\n에너지대전**")
        st.markdown("📅 **2026. 09. 16 ~ 09. 18**\n📍 **부산 BEXCO**")
        img_url3 = "https://koreaenergyshow.energy.or.kr/display.do?name=%ea%b5%ad%eb%ac%b4%ec%b4%9d%eb%a6%ac%eb%8b%98+%ec%88%9c%eb%9e%8c(6).JPG&folder=202509&dir_folder=board_gallery"
        st.markdown(f'<div style="width: 100%; height: 180px; overflow: hidden; border-radius: 8px; margin-bottom: 5px;"><img src="{img_url3}" style="width: 100%; height: 100%; object-fit: cover;"></div>', unsafe_allow_html=True)
        st.write("---")
        st.markdown("* 고효율 ICT 솔루션\n* 데이터센터 ESS 연계\n* 분산에너지 활성화")
        st.link_button("상세 보기", "https://koreaenergyshow.energy.or.kr/main/main.do", use_container_width=True)

# [안내 문구]
st.markdown("""
    <div style="background-color: #f8f9fa; border-left: 5px solid #FF4B4B; padding: 15px; border-radius: 5px; margin-top: 10px;">
        <p style="margin: 0; color: #555555; font-size: 0.9em;">
            💡 <b>안내:</b> 일정과 장소는 주최측 사정에 따라 변동될 수 있습니다. 참석 전 공식 홈페이지 확인을 권장드립니다.
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# --- 4. [Real Tip] 1분 실무 체크리스트: 누전(지락) 관리 ---
st.markdown("## ⚡ 실무 꿀팁: 누전(지락) 메커니즘과 검출 장치")

with st.container(border=True):
    st.markdown("### **💦 수도꼭지 비유로 이해하는 누전 원리**")
    
    # 열 비율을 [2, 1]에서 [1.5, 1] 또는 [1.2, 1]로 조정하여 수식을 왼쪽으로 당김
    # gap="small"을 추가하여 열 사이의 빈 공간을 최소화합니다.
    col_desc, col_formula = st.columns([1.2, 1], gap="small")
    
    with col_desc:
        st.write("""
        **전기 회로의 대원칙은 '들어간 만큼 나와야 한다'는 키르히호프의 전류 법칙(KCL)입니다.**
        
        - **정상:** 수도꼭지로 보낸 물이 10L일 때 배수구로 나오는 물도 10L인 상태입니다.
        
        - **누전:** 보낸 건 10L인데 9L만 돌아온다면? 중간에 파이프가 터져 1L가 샌 것입니다.
        
        - 이처럼 벡터 합이 0이 되지 않고 남는 전류를 **영상 전류($I_0$)**라고 부릅니다.
        """)

    with col_formula:
        # 수식을 왼쪽으로 더 밀기 위해 정렬을 'left'로 변경하거나 마진 조정
        st.markdown("<div style='margin-top: -25px; margin-left: -40px;'>", unsafe_allow_html=True)
        
        # 1. 수식 출력
        st.latex(r"I_r + I_s + I_t + I_n = I_0 \neq 0")
        
        # 2. 캡션 출력 (수식과 정렬을 맞추기 위해 text-align 유지)
        st.markdown("""
            <div style="text-align: center; margin-top: -20px; margin-left: 40px;">
                <p style="font-size: 0.85em; color: gray;">지락 발생 시 전류의 불균형</p>
            </div>
        """, unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # ZCT vs NCT 비교
    st.markdown("#### **🔍 누전을 찾는 '두 개의 눈': ZCT vs NCT**")
    col_zct, col_nct = st.columns(2)
    with col_zct:
        st.markdown("**① ZCT (영상변류기)**")
        st.write("- **위치:** 3상 4선 전체를 도넛처럼 감쌈\n- **용도:** 일반적인 지락 차단 및 경보 (ELB, ELD)")
    with col_nct:
        st.markdown("**② NCT (중성점 변류기)**")
        st.write("- **위치:** 변압기 중성점과 대지 접지선 사이\n- **용도:** 상위 계통 및 변압기 자체 보호")



# 2. 데이터센터의 난제: Igr vs Igc (진짜 vs 가짜)
with st.expander("⚠️ [심화] 분명 메거는 정상인데 알람이 울린다면?", expanded=True):
    st.markdown("""
    데이터센터에서 ELD가 울리는데 절연 저항은 정상인 경우가 많습니다. 범인은 **용량성 누설전류($I_{gc}$)**입니다.
    
    - **$I_{gr}$ (저항성):** 피복 손상 등 진짜 절연 파괴. **화재/감전의 원인.**
    - **$I_{gc}$ (용량성):** 서버 SMPS 필터나 긴 케이블에 의해 흐르는 **노이즈성 전류.**
    
    **✅ 해결책:** 일반 클램프 미터 대신 **'Igr 전용 누설전류계'**를 사용하세요. 가짜 누전($I_{gc}$)을 걸러내고 진짜 위험($I_{gr}$)만 찾아낼 수 있습니다.
    """)

# 3. 실무 체크리스트 (기존 코드 보강)
with st.expander("🛠️ 현장 점검 핵심 포인트", expanded=True):
    st.markdown("""
    - **ZCT 설치 주의:** 접지선(Earth Wire)이 ZCT를 통과하면 지락 전류가 상쇄되어 검출되지 않습니다.
    - **케이블 쉴드 접지:** 쉴드선을 접지할 때 ZCT를 통과했다면 반드시 다시 전단으로 되돌려 빼주어야 합니다.
    - **ELD 동작 시:** 데이터센터처럼 무중단이 중요한 곳은 섣불리 차단기를 내리지 말고, 하위 분기 회로를 찍어보며 범인 회로를 색출하는 것이 먼저입니다.
    """)

# --- 5. [Must Visit] 전기인이라면 꼭 가봐야 할 곳 ---
st.markdown("## 🏛️ 전기인 성지 순례: 영감과 휴식의 공간")

with st.container(border=True):
    # 1. 한국전기박물관 섹션
    st.markdown("### **1. 전기의 역사와 미래를 만나다: 한국전기박물관**")
    
    col_img1, col_txt1 = st.columns([1, 1.8])
    
    with col_img1:
        # 공식 웹사이트 이미지 경로 반영
        st.image("https://www.kepco.co.kr/assets/art/images/pages/space/museum/museum_swiper_01.png", 
                 caption="대한민국 전력 산업의 발자취 (한전아트센터 내)")
    
    with col_txt1:
        st.write("""
        우리가 매일 다루는 전기가 우리나라에 처음 어떻게 들어왔는지 알고 계신가요? 
        서울 서초동 한전아트센터 내에 위치한 **'한국전기박물관'**은 국내 유일의 전기 전문 박물관입니다.
        
        * **주요 볼거리:**
            - **에디슨의 유산:** 전기의 아버지가 만든 진품 전구와 초기 가전제품 전시
            - **전력 계통의 변천사:** 과거의 애자, 변압기부터 현대의 스마트 그리드까지 총망라
            - **특화 전시:** 전력 산업의 역사적 사료와 미래 에너지 기술 체험
        """)
        # 링크 다음 줄에 주소 배치
        st.markdown("""
        🔗 **[공식 홈페이지 방문하기](https://www.kepco.co.kr/art/space/museum/museumList.do)** \n\n📍 **주소:** 서울특별시 서초구 효령로72길 60 (한전아트센터 내)  
        ⏰ **관람:** 10:00 ~ 18:00 (매주 월요일 휴관 / 관람료 무료)
        """)

    st.markdown("<hr style='margin: 20px 0; border: 0.5px solid #ddd;'>", unsafe_allow_html=True)

    # 2. 마포새빛문화숲 섹션
    st.markdown("### **2. 도심 속 발전소의 변신: 마포새빛문화숲 (당인리)**")
    
    col_img2, col_txt2 = st.columns([1, 1.8])
    
    with col_img2:
        # 이미지가 준비되지 않았을 때를 대비한 샘플 이미지 또는 경로 처리
        # 실제 경로를 입력하실 때는 st.image("/home/user/my_portal/image/mapo.png") 형태로 넣으시면 됩니다.
        try:
            st.image("image/mapo.png", caption="벚꽃 터널로 유명한 당인리 발전소 전경")
        except:
            st.warning("🖼️ 이미지를 준비 중입니다. (mapo.png 경로 확인 필요)")
        
    with col_txt2:
        st.write("""
        공학적 지식도 좋지만, 전력 설비가 도심 속에서 어떻게 시민들과 어우러지는지 느껴보는 것은 어떨까요? 
        세계 최초로 **지하에 건설된 대용량 화력발전소** 위에 조성된 이 공원은 전기인들에게 특별한 자부심을 줍니다.
        
        * **방문 포인트:**
            - **벚꽃 명소:** 발전소 정문부터 이어지는 서울의 숨겨진 벚꽃 터널 (3~4월 강추)
            - **코미포 에너지움:** 발전소 내 에너지 홍보관에서 지하 발전소의 기술력 확인
            - **리프레시 공간:** 당인리 화력발전소 4·5호기 자리에 펼쳐진 탁 트인 한강 조망 공원
        """)
        # 링크 다음 줄에 주소 배치
        st.markdown("""
        🔗 **[상세 정보(Visit Seoul)](https://korean.visitseoul.net/area/2024-maposaebit/KOPjxg13l)** \n\n📍 **주소:** 서울특별시 마포구 토정로 56  
        🌳 **관람:** 공원 구역 연중무휴 개방 (에너지움은 사전 예약 권장)
        """)

    # 하단 팁
    st.info("💡 **전기인 전용 팁:** 한국전기박물관은 주차 시설이 넉넉해 가족 나들이로 좋습니다. 마포새빛문화숲 방문 시에는 인근 상수동 카페거리와 연계해 전력 기술의 현대적 공존을 느껴보세요!")

st.markdown("<br>", unsafe_allow_html=True)

# --- 6. [Closing] Q&A 및 푸터 ---
st.divider()
col_qa, col_info = st.columns(2)

with col_qa:
    st.markdown("### 💬 Q&A: 현장의 목소리")
    # 단순 문답에서 실무적인 팁을 포함한 심층 답변으로 보강
    with st.expander("Q: 터보냉동기 프리쿨링 전환 시점은 언제인가요?", expanded=True):
        st.write("""
        **A: 외기 온도가 냉수 환수 온도보다 2~3℃ 낮아지는 늦가을부터가 적기입니다.** 하지만 단순히 온도만 보기보다는 **'열교환기 입구 온도'**와 **'냉동기 압축기 동력'**의 평형점을 찾는 것이 중요합니다. 
        우리 센터처럼 **별도 열교환기**가 설치된 경우, 외기 온도가 충분히 낮지 않더라도 **혼합 방식(Partial Free Cooling)**을 통해 냉동기 부하를 선제적으로 줄여 에너지를 절감할 수 있습니다. 
        """)

with col_info:
    st.markdown("### 📅 Next Issue: Vol. 06 예고")
    # 다음 호에 다룰 구체적인 기술 포인트들을 나열하여 기대감 형성
    st.success("""
    **주제: '데이터센터 에너지 절약의 핵심, 프리쿨링(Free Cooling) 운용 전략'**
    
    * **혼합 모드 vs 전프리쿨링 모드:** 전환 기준점 잡기
    * **중간 버퍼탱크의 역할:** 정전 시 백업 이상의 에너지 효율 관리
    * **수질 관리:** 옥탑 냉각탑 동파 방지와 열교환기 스케일 관리
    """)
