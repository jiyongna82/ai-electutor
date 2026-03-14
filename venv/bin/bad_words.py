# bad_words.py

BAD_WORDS = [
    # 1. 한국어 욕설 및 비하 표현
    "시발", "씨발", "개새끼", "병신", "존나", "지랄", "꺼져", "미친",
    "ㅅㅂ", "ㅂㅅ", "ㅈㄴ", "ㄲㅈ", "ㅗ", "ㄴㅁ", "ㅁㅊ", "ㅅㄲ",
    "한남", "한녀", "틀딱", "급식충", "개독", "좌빨", "우좀",

    # 2. 성인 및 음담패설
    "섹스", "섹스해", "야동", "성인물", "포르노", "자위", "조건만남", 
    "오빠랑", "출장마사지", "성매매", "바다이야기", "토토", "도박",
    "sex", "porn", "poker", "casino", "viagra", "cialis", "adult",

    # 3. 스팸 및 광고
    "광고문의", "무료증정", "수익보장", "카톡상담", "고수익", "재테크알바",
    "buy now", "click here", "free money", "bitcoin mining", "investment",
    "대출", "금리최저", "수익인증", "카지노"
]

def check_bad_words(text):
    """
    텍스트 내에 금지어가 포함되어 있는지 검사 (공백 제거 후 검사)
    """
    if not text:
        return False, None
    clean_text = text.replace(" ", "").lower()
    for word in BAD_WORDS:
        if word in clean_text:
            return True, word
    return False, None