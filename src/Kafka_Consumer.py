#对未消费的信息进行消费，并统计队列中这次消费了多少
import time

timeout_seconds = 5  # 超时限制，5秒
start_time = time.time()

message_count = 0



from confluent_kafka import Consumer, KafkaException, KafkaError

# 配置消费者
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka 集群的地址
    'group.id': 'test_group',  # 消费者组
    'auto.offset.reset': 'earliest'  # 从最早的消息开始消费
}

# 创建消费者实例
consumer = Consumer(conf)

# 订阅主题
consumer.subscribe(['test_topic'])

try:
    while True:
        msg = consumer.poll(timeout=1.0)  # 等待1秒钟查看消息
        if msg is None:
            if time.time() - start_time > timeout_seconds:
                print("No new messages for 5 seconds. Exiting.")
                break
            continue  # 没有新消息
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # 到达分区末尾
                continue
            else:
                raise KafkaException(msg.error())
        
        # 每消费到一条消息，计数器加一
        message_count += 1
        print(f"Consumed message: {msg.value().decode('utf-8')}")
except KeyboardInterrupt:
    pass
finally:
    # 关闭消费者
    consumer.close()

# 打印消费的消息数量
print(f"Total messages consumed: {message_count}")
