#!/usr/bin/env python3
import time
import rovos
from std_msgs import Float32

class TalkerNode(rovos.Node):
    def __init__(self):
        super().__init__("talker")

        self.publisher = self.create_publisher(Float32, "sensor_data")

        self.counter = 0.0

    def send_data(self):
        msg = Float32()
        msg.data = self.counter

        self.publisher.publish(msg)
        rovos.success(f"Mengirim data: {msg.data}")

        self.counter += 1.1

if __name__ == "__main__":
    node = TalkerNode()

    try:
        while True:
            node.send_data()
            time.sleep(1)
    except KeyboardInterrupt:
        node.shutdown()