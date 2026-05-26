"""
Shared text cleaning helpers for all exporters.
"""

SPAM_KEYWORDS = [
    "( yaaaaacha )",
    "มังฮวาชื่อเดียวกัน",
    "เพื่อเข้าลิงค์อ่านได้เลย หรือกดอ่านในหน้าโปรไฟล์ก็ได้",
    "yakksha.com",
    "✦ สตรีมเมอร์หวนคืน55ชาติ ✦",
    "<<< แปลชนต้นฉบับ 20 ตอนแล้ว มังฮวา 20 = นิยาย 21 เสิช",
    "✦ จักรพรรดิทรายในโลกาวินาศ ✦",
    "<<< แปลชนต้นฉบับ 20 ตอนแล้ว มังฮวา 20 = นิยาย 13 เสิช",
]
EXTRA_SPAM_KEYWORDS: list[str] = []


def get_default_spam_keywords() -> list[str]:
    return SPAM_KEYWORDS.copy()


def set_extra_spam_keywords(keywords: list[str]) -> None:
    global EXTRA_SPAM_KEYWORDS
    EXTRA_SPAM_KEYWORDS = [k.strip() for k in keywords if k and k.strip()]


def clean_text_line(text: str) -> str:
    cleaned = text.strip()
    for keyword in SPAM_KEYWORDS + EXTRA_SPAM_KEYWORDS:
        cleaned = cleaned.replace(keyword, "")
    return cleaned.strip()
