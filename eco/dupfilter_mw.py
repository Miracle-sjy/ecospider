import redis
from scrapy.utils.request import RequestFingerprinter
from scrapy.exceptions import IgnoreRequest
##断点重爬
class RedisDupFilterMiddleware:
    def __init__(self, redis_url, key='dup:fingerprint'):
        self.r = redis.from_url(redis_url)
        self.key = key
        self.finger = RequestFingerprinter()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.get('REDIS_URL'))

    def process_request(self, request, spider):
        fp = self.finger.fingerprint(request).hex()    # Scrapy 内置 URL 指纹
        if self.r.sismember(self.key, fp):
            spider.logger.debug(f"Dropped already seen: {request.url}")
            raise IgnoreRequest
        # 等 Response 成功后再记指纹（防失败被标已爬）
        request.meta['fp'] = fp
        return None

    def process_response(self, request, response, spider):
        if response.status == 200 and 'fp' in request.meta:
            self.r.sadd(self.key, request.meta['fp'])
        else:
            spider.logger.debug(f"Status {response.status}, not marking seen")
        return response