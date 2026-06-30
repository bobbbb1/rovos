# core/publisher.py
# from cyclonedds.topic import Topic
# from cyclonedds.pub import Publisher as DDSPublisher, DataWriter
from core.protocol import Topic, DDSPublisher, DataWriter

class Publisher:
    def __init__(self, node, msg_type, topic_name: str, qos=None):
        self.node = node
        self.msg_type = msg_type
        self.topic_name = topic_name

        self.topic = Topic(self.node.participant, self.topic_name, self.msg_type)
        self.dds_publisher = DDSPublisher(self.node.participant)
        
        self.writer = DataWriter(self.dds_publisher, self.topic, qos=qos)

    def publish(self, msg):
        if not isinstance(msg, self.msg_type):
            raise TypeError(f"Data harus bertipe {self.msg_type.__name__}")

        self.writer.write(msg)