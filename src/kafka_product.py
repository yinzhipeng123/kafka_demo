#生产者产生一个消息
from confluent_kafka import Producer

# 配置生产者
conf = {
    'bootstrap.servers': 'localhost:9092',  # Kafka 集群的地址
    'acks': 'all'  # 等待所有副本确认
}

# 创建生产者实例
producer = Producer(conf)

# 发送消息的回调函数
def delivery_callback(err, msg):
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))

# 发送消息到 Kafka
def send_message(topic, key, value):
    # 使用 str.encode 进行消息内容的序列化
    producer.produce(topic, key=key.encode('utf-8'), value=value.encode('utf-8'), callback=delivery_callback)
    producer.flush()  # 确保消息被发送完毕

# 示例：发送一条消息
send_message('test_topic', 'key1', 'value1')

# 删除 producer.close()，因为并不需要
