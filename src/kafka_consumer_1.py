#一次就消费一个消息，然后推出
from confluent_kafka import Consumer, KafkaException, KafkaError

# 配置消费者
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka 集群地址
    'group.id': 'my-consumer-group',         # 消费者组 ID
    'auto.offset.reset': 'earliest'          # 从最早的消息开始消费
}

# 创建消费者实例
consumer = Consumer(conf)

# 订阅主题
topic = 'test_topic'
consumer.subscribe([topic])

try:
    # 只消费一个消息
    msg = consumer.poll(timeout=1.0)  # 超时时间为 1 秒

    if msg is None:
        print("没有新消息")
    elif msg.error():
        if msg.error().code() == KafkaError._PARTITION_EOF:
            # 这个错误表示到达了分区的末尾
            print(f"End of partition {msg.partition} reached {msg.offset}")
        else:
            raise KafkaException(msg.error())
    else:
        # 正常消费到的消息
        print(f"Received message: {msg.value().decode('utf-8')}")

except KeyboardInterrupt:
    print("消费被中断")

finally:
    # 关闭消费者
    consumer.close()
