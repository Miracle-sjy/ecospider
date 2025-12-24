# 🕷️ eco – 分布式 Scrapy-Redis 爬虫框架

> 一套「开箱即用、插件化、可水平扩展」的通用爬虫骨架，以 Scrapy-Redis 为核心，支持多站点、多算法、自动参数刷新与 Docker 一键部署。

---

## 📦 核心能力

| 模块             | 特性                                  | 状态 |
| ---------------- | ------------------------------------- | ---- |
| **Scrapy-Redis** | 分布式调度、去重、断点续爬            | ✅    |
| **插件化解密**   | `eco/decode/<site>.py` 单文件即一站点 | ✅    |
| **自动刷新**     | Token/签名/时间戳失效自动重计算       | ✅    |
| **代理池**       | 中间件级动态切换                      | ✅    |
| **MongoDB**      | 默认持久化（支持管道复写）            | ✅    |
| **Docker**       | 开发/生产同一镜像                     | ✅    |
| **Kafka**        | 可选消息队列导出                      | ✅    |

---

## 🚀 5 分钟上手指南

### 1. 本地调试
```bash
git clone <repo>
cd eco
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 示例：闲鱼 Feed
redis-cli lpush xianyu:start_urls 1
scrapy crawl xianyu
```

### 2. 插件开发（新增站点）
```bash
# 1) 解密插件
cat > eco/decode/foo.py <<'EOF'
def sign(inputs: dict) -> str:
    return hashlib.md5(f"{inputs['key']}{inputs['t']}".encode()).hexdigest()
EOF

# 2) Spider（name=文件名）
cat > eco/spiders/foo_feed.py <<'EOF'
from scrapy_redis.spiders import RedisSpider
class FooFeedSpider(RedisSpider):
    name = "foo"
    redis_key = "foo:start_urls"
EOF

# 3) 推入 Redis
redis-cli lpush foo:start_urls 1
```

**无需改动工厂、无需重启服务** —— 插件即插即用。

---

## 📁 项目结构

```
eco/                      # 项目根
├── eco/                  # 核心包
│   ├── decode/           # 插件化解密 ← 单文件 = 单站点
│   ├── spiders/          # Spider 集合
│   ├── middlewares.py    # 代理·指纹·签名·Token 刷新 一条链
│   ├── pipelines.py      # Mongo 默认落地 + Kafka 导出
│   ├── settings.py       # 分布式、Redis、代理、Mongo 全配置
│   ├── exceptions.py     # 自定义异常（TokenRefreshException）
│   ├── fingerprints.py   # UA / 指纹生成库
│   ├── items.py          # 统一 Item 定义
│   ├── models.py         # Mongo 集合映射（可选 ODM）
│   ├── extensions.py     # Scrapy 扩展钩子（监控、统计）
│   └── starturl_redis.py # 脚本：向 Redis 灌起始 URL
├── .github/              # CI 工作流：测试 + 镜像构建
├── docker-compose.yml    # 一键集群（Scrapy-Redis + Mongo + Kafka）
├── Dockerfile            # 含 Chrome 的瘦镜像
├── requirements.txt      # 依赖锁定
├── scrapy.cfg            # Scrapy 项目标识
├── .gitignore        # 忽略 venv / pyc / log
├── proxies.txt           # 代理池列表（ip:port 每行）
├── monitor.yml           # Prometheus 指标导出（可选）
├── kafka_consumer.py     # 示例：消费 Kafka 结果
└── kafkatest.py          # Kafka 连通性快速测试
```
---

## 🔌 //插件接口约定

| 文件名      | 必须实现                    | 可选                             |
| ----------- | --------------------------- | -------------------------------- |
| `<site>.py` | `sign(inputs: dict) -> str` | `refresh_inputs(inputs) -> dict` |

工厂 3 行代码，运行时 `importlib` 动态加载：

```python
from eco.decode import get_signer
sign = get_signer(spider.name)   # 返回模块，直接调 sign(...)
```

---

## 🔄 //自动参数刷新

Spider 抛出 `TokenRefreshException` →  
`RetrySignMiddleware` 自动调用插件的 `refresh_inputs()` →  
生成新 `t`、`sign`、`Cookie` 并重试，**无人值守**。

---

## 🐳 生产部署

```bash
# 单节点
docker-compose up -d

# 扩容爬虫
docker-compose up -d --scale crawler=4
```

镜像已含 Chrome、依赖、代码；挂载卷即可热更新插件。

---

## 📊 监控 & 日志

- Scrapy 默认日志 + Redis 统计  
- 可选 Prometheus Exporter（见 `monitor.yml`）  
- Kafka 导出实时数据流（`kafka_consumer.py` 示例）

---

## 🤝 //参与贡献

1. Fork 仓库  
2. 新建 `feat/foo` 分支  
3. 提交插件或核心改进  
4. PR → CI 自动跑单元测试 & 镜像构建

---

## 📄 许可证

MIT © 2024 eco-org





# ✅ 已完成 
1. **分布式调度**  
   - Scrapy-Redis 队列，支持 `docker compose up --scale scrapy=N`  
2. **流式数据链路**  
   - Kafka Topic：`scrapy.quotes_spider` → Consumer → Mongo  
3. **字段清洗 & 校验**  
   - `pydantic` 模型，非法数据自动丢弃  
4. **断点续爬 & 增量去重**  
   - Redis 指纹集合，仅 200 响应才记录，重启不重复  
5. **一键基础设施**  
   - `docker-compose.yml` 含 Redis + Kafka + Mongo，裸机/容器互通  
6. **辅助脚本**  
   - `push_start_urls.py` 一键灌 URL  
   - `kafka_consumer.py` 消费落库  

# ❌ 未完成
| 编号   | 功能 | 描述                                   | 备注 |
|------|----|--------------------------------------|----|
| A    | 代理池 + 失败重试 | 文件/免费 API 自动换 IP                     |
| B完成！ | 监控仪表盘 | Redis → Grafana 实时曲线 + 告警            |
| C完成！ | 自动打包 & CI | GitHub Actions：push tag → 镜像 → 部署    |
| D    | 多站点（books）  | 独立队列/Topic/集合，一键加第 3 站               |
| E    | 字段加密/脱敏  | 敏感字段落库前哈希或打码                         |
| F    | 限速自适应  | 按失败率动态调整并发 & 延迟                      |
| G    | 数据双写 | 同时写 Mongo + ES / ClickHouse          |
| H    | 健康探针  | `/health` 接口，K8s 自动重启                |
| I    | 单元测试 & CI  | `pytest` + `scrapy.contracts`，PR 自动跑 |

监控部分可以加普罗米修斯更完善