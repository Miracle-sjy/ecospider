from kafka import KafkaConsumer
import json
from pymongo import MongoClient

consumer = KafkaConsumer(
    'scrapy.spider',
    bootstrap_servers=['localhost:9092'],
    auto_offset_reset= 'earliest',
    enable_auto_commit=True,
    group_id='mongo-store',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

mongo = MongoClient('mongodb://localhost:27018')  #端口映射
coll = mongo['scrapy']['eco']

for msg in consumer:
    coll.insert_one(msg.value)
    print('saved',msg.value)