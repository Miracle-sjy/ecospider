# 官方 Python 镜像
FROM python:3.11-slim

WORKDIR /app

# 装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制源码
COPY . .

# 默认命令：等待 Redis 队列，有 URL 就爬
CMD ["scrapy", "crawl", "quotes_spider"]