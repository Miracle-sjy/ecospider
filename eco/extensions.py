import redis, time, threading
from scrapy import signals
##监控
class StatsPusher:
    def __init__(self, redis_url, interval=5):
        self.r = redis.from_url(redis_url)
        self.interval = interval

    @classmethod
    def from_crawler(cls, crawler):
        ext = cls(crawler.settings.get('STATS_REDIS', 'redis://localhost:6380'))
        crawler.signals.connect(ext.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(ext.spider_closed, signal=signals.spider_closed)
        crawler.signals.connect(ext.item_scraped, signal=signals.item_scraped)
        return ext

    def spider_opened(self, spider):
        self.key = f"stats:{spider.name}"
        self._loop()

    def item_scraped(self, item, response, spider):
        self.r.hincrby(self.key, "item_scraped", 1)

    def _loop(self):
        # 每 5 秒写一次时间序列
        stats = self.r.hgetall(self.key)
        stats["ts"] = int(time.time())
        self.r.xadd(f"series:{self.key}", stats, maxlen=86400)  # 保留 24h
        threading.Timer(self.interval, self._loop).start()

    def spider_closed(self, spider):
        self.r.hset(self.key, "finish_reason", "finished")