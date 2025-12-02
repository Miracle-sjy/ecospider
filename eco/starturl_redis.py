#!/usr/bin/env python3
import redis
import sys

# ===== 可改配置 =====
REDIS_URL = "redis://localhost:16379"   # 与 settings.py 保持一致
QUEUE_KEY  = "quotes_spider:start_urls" # 与 spider 的 redis_key 一致
URLS       = [                        # 想灌的 URL 列表
    "https://quotes.toscrape.com/",
    "https://quotes.toscrape.com/page/2/",
]
# ====================

def push():
    r = redis.from_url(REDIS_URL)
    # 先清旧队列（可选）
    r.delete(QUEUE_KEY)
    # 批量 lpush
    r.lpush(QUEUE_KEY, *URLS)
    n = r.llen(QUEUE_KEY)
    print(f"✅ 已推送 {len(URLS)} 条 URL 到 {QUEUE_KEY}，当前队列长度：{n}")

if __name__ == "__main__":
    push()