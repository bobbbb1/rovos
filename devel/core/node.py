# core/node.py
import os
import yaml
import sys
import time
import json
import tempfile
import signal
import atexit
from pathlib import Path
from typing import Type, Callable, Optional

from core.protocol import DomainParticipant, IdlStruct

import core.debug as rovos

ROVOS_REGISTRY = Path(tempfile.gettempdir()) / "rovos2_topology.json"

class Node:
    def __init__(self, node_name: str):
        """
        Inisialisasi Node ROVOS berbasis Eclipse CycloneDDS.
        Every node otomatis bertindak sebagai DomainParticipant yang mandiri (p2p).
        """
        self.name = node_name
        self._unregistered = False
        self._my_topics = []
        self.running = True
        
        if len(sys.argv) > 1 and not sys.argv[1].endswith('.py'):
            self.config_path = sys.argv[1]
        else:
            self.config_path = None

        try:
            self.participant = DomainParticipant()
        except Exception as e:
            rovos.error(f"[{self.name}] Gagal menginisialisasi DDS Participant: {e}")
            sys.exit(1)

        self._readers = []

        self._register_entity("node", self.name, "-")

        # JAMINAN MUTLAK 1: Registrasi pembersihan saat script exit normal
        atexit.register(self._unregister_node)

        # JAMINAN MUTLAK 2: Tangkap sinyal terminasi OS (Ctrl+C atau kill command)
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handler khusus saat menerima sinyal Ctrl+C dari OS"""
        rovos.warn(f"User interrupted the shutdown process ({signum})")
        self._unregister_node()
        sys.exit(0)

    def _register_entity(self, entity_type: str, name: str, data_type: str):
        """
        Fungsi internal untuk melakukan kloning/pencatatan pasif terhadap 
        topik dan node yang sedang aktif di sistem lokal.
        """
        try:
            # Pastikan jika file korup/kosong, kita reset ke struktur default
            data = {"nodes": [], "topics": {}}
            if ROVOS_REGISTRY.exists() and ROVOS_REGISTRY.stat().st_size > 0:
                with open(ROVOS_REGISTRY, "r") as f:
                    try:
                        data = json.load(f)
                    except Exception:
                        pass

            if "nodes" not in data: data["nodes"] = []
            if "topics" not in data: data["topics"] = {}

            if entity_type == "node":
                if name not in data["nodes"]:
                    data["nodes"].append(name)
            
            elif entity_type == "topic":
                data["topics"][name] = data_type
                # TAMBAHAN 2: Jika node ini mendaftarkan topik, ingat namanya
                if name not in self._my_topics:
                    self._my_topics.append(name)

            # JAMINAN AMAN: Tulis ke file temporary dulu agar tidak korup 0 bytes
            temp_registry = ROVOS_REGISTRY.with_suffix(".tmp")
            with open(temp_registry, "w") as f:
                json.dump(data, f, indent=4)
            
            # Ganti file asli secara instan di level OS
            os.replace(temp_registry, ROVOS_REGISTRY)
                
        except Exception:
            pass

    def create_publisher(self, msg_type: Type[IdlStruct], topic_name: str, qos=None):
        """
        Fungsi untuk membuat Publisher baru pada topik tertentu dengan dukungan QoS.
        """
        from core.publisher import Publisher
        
        pub = Publisher(self, msg_type, topic_name, qos=qos)
        self._register_entity("topic", topic_name, msg_type.__name__)
        return pub

    def create_subscriber(self, msg_type: Type[IdlStruct], topic_name: str, callback: Callable, qos=None):
        """
        Fungsi untuk membuat Subscriber baru pada topik tertentu dengan dukungan QoS.
        """
        from core.subscriber import Subscriber
        
        sub = Subscriber(self, msg_type, topic_name, callback, qos=qos)
        self._readers.append(sub) 

        self._register_entity("topic", topic_name, msg_type.__name__)
        return sub

    def _unregister_node(self):
        """Fungsi untuk menghapus node ini dari registry saat shutdown"""
        if self._unregistered:
            return

        try:
            if ROVOS_REGISTRY.exists() and ROVOS_REGISTRY.stat().st_size > 0:
                with open(ROVOS_REGISTRY, "r") as f:
                    try:
                        data = json.load(f)
                    except Exception:
                        data = {"nodes": [], "topics": {}}

                # 1. Hapus nama node ini dari daftar aktif
                if "nodes" in data and self.name in data["nodes"]:
                    data["nodes"].remove(self.name)

                # 3. TAMBAHAN 3: Setiap node bertanggung jawab menghapus topik miliknya sendiri
                if "topics" in data:
                    for topic in self._my_topics:
                        if topic in data["topics"]:
                            del data["topics"][topic]

                # Jaga-jaga: Jika seluruh node sudah habis, sapu bersih total
                if not data["nodes"]:
                    data["topics"] = {}

                # Tulis secara atomic
                temp_registry = ROVOS_REGISTRY.with_suffix(".tmp")
                with open(temp_registry, "w") as f:
                    json.dump(data, f, indent=4)
                
                os.replace(temp_registry, ROVOS_REGISTRY)
        except Exception:
            pass

        finally:
            self._unregistered = True

    def spin(self):
        """
        Menjaga agar Node tetap hidup dan terus mendengarkan data
        """
        print(f"[{self.name}] Node berjalan... Tekan Ctrl+C untuk stop.")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

    # Di dalam core/node.py pada class Node
    def load_config(self, relative_path=None):
        """
        Membaca file YAML. Prioritas pertama dari environment ROVOS_CONFIG_PATH (jika lewat launch file),
        Prioritas kedua baru berdasarkan path relatif dari file skrip yang memanggilnya.
        """
        # 1. Cek dulu apakah ada jalur absolut otomatis dari rovos2 launch
        config_path = os.environ.get("ROVOS_CONFIG_PATH")

        # 2. Kalau gak ada (berarti di-run satuan), pakai logika relative_path asli motodemu
        if not config_path and relative_path:
            main_script_path = os.path.abspath(sys.argv[0])
            node_dir = os.path.dirname(main_script_path)
            config_path = os.path.join(node_dir, relative_path)

        if not config_path:
            rovos.error("Gagal memuat konfigurasi: Path YAML tidak ditentukan.")
            return None

        try:
            with open(config_path, "r") as f:
                print(f"[*] Berhasil memuat konfigurasi dari {os.path.basename(config_path)}")
                return yaml.safe_load(f)
        except Exception as e:
            rovos.error(f"Gagal membaca file YAML di {config_path}. Error: {e}")
            return None
        
    def shutdown(self):
        """Fungsi untuk mematikan node dan thread"""
        if not self.running:
            return
            
        self.running = False
        rovos.warn(f"Shutdown process has finished cleanly")
        
        # OTOMATISASI UNTUK OBJEK HARDWARE (Joystick/Serial)
        if hasattr(self, 'device') and self.device:
            try:
                self.device.close()
                rovos.info(f"Koneksi hardware pada [{self.name}] berhasil diputus.")
            except Exception:
                pass

        # BARU: OTOMATISASI UNTUK OBJEK KAMERA OPENCV (Stream Node)
        for cap_attr in ['cap1', 'cap2']:
            if hasattr(self, cap_attr):
                cap_obj = getattr(self, cap_attr)
                if cap_obj is not None:
                    try:
                        cap_obj.release()
                        rovos.info(f"Resource {cap_attr} pada [{self.name}] berhasil dilepas.")
                    except Exception:
                        pass

        # Jalankan pembersihan sisa topik di JSON topology registry
        self._unregister_node()