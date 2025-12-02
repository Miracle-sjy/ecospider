# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from kafka import KafkaProducer
from eco.models import EcoModel
from pydantic import ValidationError
import json

class ValidationPipeline:
    def process_item(self, item, spider):
        try:
            # 把 Item 转成 dict 校验
            valid = EcoModel(**item)
            # 校验通过，把干净数据写回 Item
            item["text"] = valid.text
            item["author"] = valid.author
            item["tags"] = valid.tags
            return item
        except ValidationError as e:
            # 脏数据直接丢弃 + 日志
            spider.logger.warning(f"Invalid item dropped: {e}  raw={dict(item)}")
            return None      # 返回 None 即丢弃


class KafkaPipeline:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=['localhost:9092'],  #宿主机端口
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def process_item(self,item,spider):
        self.producer.send('scrapy.spider',dict(item))
        return item

    def close_spider(self,spider):
        self.producer.close()

# class EcoPipeline:
#     def process_item(self, item, spider):
#         return item

class MongoPipeline:
    def __init__(self):
        # 连本地 27017，默认没有密码
        self.client = MongoClient("mongodb://localhost:27018")
        self.db = self.client["scrapy"]      # 数据库
        self.coll = self.db["eco"]        # 集合
        print("=== MongoPipeline connected, collection:", self.coll)

    def process_item(self, item, spider):
        print("=== process_item called, item:", item)
        # 把 Item 转成 dict 直接插入
        self.coll.insert_one(ItemAdapter(item).asdict())
        return item

    def close_spider(self, spider):
        self.client.close()