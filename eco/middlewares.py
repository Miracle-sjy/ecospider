# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random
import base64
from eco import settings
import time
from eco.fingerprints import random_headers

from eco.decode import get_signer
from eco.exceptions import TokenRefreshException

class TokenRefreshMiddleware:
    """
        通用刷新器：只认 TokenRefreshException，
        具体刷新逻辑全交给插件模块。
    """
    """
        捕获 TokenRefreshException 并自动重算参数
    """
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_exception(self, request, exception, spider):
        if not isinstance(exception, TokenRefreshException):
            return None   # 其他异常不管

        # 让插件刷新
        signer = get_signer(spider.name)
        old = {
            "token": request.meta.get("token", ""),
            "t": request.meta.get("t", ""),
            "appKey": spider.api_key,
            "data": request.meta["data_str"],
            "sign": request.meta.get("sign", ""),
        }
        new = signer.refresh_inputs(old)

        # 替换 URL
        url = request.url
        for k in ("t", "sign"):
            if old.get(k) and new.get(k):
                url = url.replace(f"{k}={old[k]}", f"{k}={new[k]}")

        # 更新 meta & Cookie
        request.meta.update(token=new["token"], t=new["t"], sign=new["sign"])
        request.cookies.update(new.get("cookies", {}))

        spider.logger.info("[Refresh] 已重签，重新入队")
        return request.replace(url=url)

    def process_response(self, request, response, spider):
        # 按响应内容触发刷新
        if "FAIL_SYS_TOKEN" in response.text:
            raise TokenRefreshException
        return response
class SignMiddleware:
    """
       首次签名：把 meta 里的占位符换成真正的 sign、t、cookie
    """
    """
        只干一件事：把 URL 里的 PLACEHOLDER 换成真正的 t 和 sign
    """
    def __init__(self, crawler):
        self.crawler = crawler

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        if "PLACEHOLDER" not in request.url:
            return None   # 已经签过，直接放行

        # 取参数
        t = str(int(time.time() * 1000))
        data_str = request.meta["data_str"]
        token = request.meta.get("token", "")

        # 签名
        sig = get_signer(spider.name).sign({
            "token": token,
            "t": t,
            "appKey": spider.api_key,
            "data": data_str
        })

        # 替换占位符
        url = request.url.replace("t=PLACEHOLDER", f"t={t}") \
                         .replace("sign=PLACEHOLDER", f"sign={sig}")

        # 写回 meta（刷新中间件要用）
        request.meta.update(t=t, sign=sig, token=token)
        spider.logger.debug(f"[Sign] t={t}  sign={sig}")
        return request.replace(url=url)
#ip池代理
class RandomProxyMiddleware:
    def __init__(self):
        with open(settings.PROXY_LIST_FILE, 'r') as f:
            self.proxies = [line.strip() for line in f if line.strip()]

    def process_request(self, request, spider):
        url = random.choice(self.proxies)
        request.meta['proxy'] = url
        spider.logger.debug(f"Use proxy: {url}")
        return None

    def process_exception(self, request, exception, spider):
        # 任何网络异常 -> 换代理重试
        spider.logger.warning(f"Proxy {request.meta.get('proxy')} failed: {exception}")
        # 把失败代理从列表踢掉（可选）
        self.proxies = [p for p in self.proxies if p != request.meta.get('proxy')]
        # 必须返回 Request 才会重试
        return request

#UA 指纹
class FingerPrintMiddleware:
    def process_request(self, request, spider):
        # 随机指纹灌进请求头
        request.headers.update(random_headers())
        spider.logger.debug(f"FP → {request.headers['User-Agent']}")
        return None

class EcoSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class EcoDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
