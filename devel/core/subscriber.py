# from cyclonedds.topic import Topic
# from cyclonedds.sub import Subscriber as DDSSubscriber, DataReader
import threading
from core.protocol import Topic, DDSSubscriber, DataReader
import time

class Subscriber:
    def __init__(self, node, msg_type, topic_name: str, callback, qos=None):
        self.node = node
        self.msg_type = msg_type
        self.topic_name = topic_name
        self.callback = callback

        self.topic = Topic(self.node.participant, self.topic_name, self.msg_type)

        self.dds_subscriber = DDSSubscriber(self.node.participant)

        self.reader = DataReader(self.dds_subscriber, self.topic, qos=qos)

        self.running = True
        self.listener_thread = threading.Thread(target=self._listener_loop, daemon=True)
        self.listener_thread.start()

    def _listener_loop(self):
        """Loop di background thread untuk mengambil paket data dari network buffer"""
        while self.running:
            try:
                sample = self.reader.take_next()
                
                if sample is not None:
                    if hasattr(sample, 'sample'):
                        actual_data = sample.sample
                    else:
                        actual_data = sample
                        
                    if actual_data is not None:
                        self.callback(actual_data)
                else:
                    time.sleep(0.01)
                    
            except Exception as e:
                print(f"[DEBUG SUB ERROR]: {e}")
                time.sleep(0.01)
            
            time.sleep(0.002)

    def destroy(self):
        """Fungsi opsional jika ingin mematikan subscriber ini secara bersih"""
        self.running = False