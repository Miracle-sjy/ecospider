scrapy+redis+kafka+mongodb





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
| 编号 | 功能 | 工作量 | 备注 |
|----|----|----|----|
| A | 代理池 + 失败重试 | 30 min | 文件/免费 API 自动换 IP |
| B | 监控仪表盘 | 10 min | Redis → Grafana 实时曲线 + 告警 |
| C | 自动打包 & CI | 20 min | GitHub Actions：push tag → 镜像 → 部署 |
| D | 多站点（books） | 30 min | 独立队列/Topic/集合，一键加第 3 站 |
| E | 字段加密/脱敏 | 15 min | 敏感字段落库前哈希或打码 |
| F | 限速自适应 | 20 min | 按失败率动态调整并发 & 延迟 |
| G | 数据双写 | 15 min | 同时写 Mongo + ES / ClickHouse |
| H | 健康探针 | 10 min | `/health` 接口，K8s 自动重启 |
| I | 单元测试 & CI | 25 min | `pytest` + `scrapy.contracts`，PR 自动跑 |

