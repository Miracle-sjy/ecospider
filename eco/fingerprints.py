import random

# 真实常见指纹
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
]

ACCEPT_LANG = ["en-US,en;q=0.9", "zh-CN,zh;q=0.9,en;q=0.8", "ja-JP,ja;q=0.9"]

ACCEPT = ("text/html,application/xhtml+xml,application/xml;q=0.9,"
          "image/avif,image/webp,image/apng,*/*;q=0.8")

def random_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": random.choice(ACCEPT_LANG),
        "Accept": ACCEPT,
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Upgrade-Insecure-Requests": "1",
    }