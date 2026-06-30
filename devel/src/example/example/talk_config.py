import rovos
from msgs.std_msgs import Int32
import time

class TalkerNode(rovos.Node):
    def __init__(self):
        super().__init__("talker_with_config")
        # Kosongkan argumennya jika dijalankan lewat 'rovos2 launch'
        # Atau isi, misal: self.load_config("../config/config.yaml")
        self.config = self.load_config()
        
        if self.config:
            # Misal di dalam config.yaml kamu ada parameter 'frequency'
            self.freq = self.config.get("frequency", 1.0)
            rovos.info(f"Menggunakan frekuensi dari config: {self.freq} Hz")
        else:
            self.freq = 1.0 # Default fallback jika config gagal diload
            rovos.warn("Config tidak ditemukan, menggunakan frekuensi default 1.0 Hz")

        self.pub = self.create_publisher(Int32, "chatter")
        
    def start(self):
        count = 0
        try:
            while True:
                msg = Int32()
                msg.data = count
                self.pub.publish(msg)
                
                rovos.log(f"Mengirim data: {msg.data}")
                
                count += 1
                
                time.sleep(1.0 / self.freq)
        except KeyboardInterrupt:
            pass

if __name__ == "__main__":
    node = TalkerNode()
    try:
        while True:
            node.start()
    except KeyboardInterrupt:
        node.shutdown()