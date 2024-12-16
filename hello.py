#加个注释
import time
import datetime
while True:

    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(current_time+" Hello")
    time.sleep(2)  # 每隔 2 秒输出一次 "Hello"
