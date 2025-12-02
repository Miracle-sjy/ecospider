from kafka import KafkaProducer
p = KafkaProducer(bootstrap_servers='localhost:9092')
future = p.send('test', b'hello')
print(future.get(timeout=3))   # 收到 RecordMetadata 说明连通
p.close()