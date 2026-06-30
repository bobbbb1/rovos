#!/usr/bin/env python3
import rovos
from msgs.std_msgs import Float32, Int32

class ListenerNode(rovos.Node):
    def __init__(self):
        super().__init__("listener")

        self.subscriber = self.create_subscriber(
            Float32, 
            "sensor_data", 
            self.callback
        )

        self.subscriber2 = self.create_subscriber(
            Int32, 
            "chatter", 
            self.callback2
        )

    def callback(self, msg):
        rovos.info(f"Menerima data: {msg.data}")

    def callback2(self, msg):
        rovos.info(f"Menerima data: {msg.data}")

if __name__ == "__main__":
    node = ListenerNode()

    try:
        while True:
            node.spin()
    except KeyboardInterrupt:
        node.shutdown()
