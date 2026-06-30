# from cyclonedds.domain import DomainParticipant
# from cyclonedds.idl import IdlStruct
# from cyclonedds.topic import Topic
# from cyclonedds.sub import Subscriber as DDSSubscriber, DataReader
# from cyclonedds.pub import Publisher as DDSPublisher, DataWriter

import os
import sys

# ========================================================
# --- BAGIAN INISIALISASI (Jangan Diubah, Sudah Sempurna) ---
# ========================================================
current_dir = os.path.dirname(os.path.abspath(__file__))

c_install_path = os.path.abspath(os.path.join(current_dir, "..", "lib", "rovosds", "install"))
os.environ["CYCLONEDDS_HOME"] = c_install_path

dll_path = os.path.join(c_install_path, "bin")
if os.path.exists(dll_path):
    os.add_dll_directory(dll_path)

python_src_path = os.path.abspath(os.path.join(current_dir, "..", "lib", "rovosds", "dds"))
if python_src_path not in sys.path:
    sys.path.insert(0, python_src_path)

import cyclonedds as rovosds
sys.modules["rovosds"] = rovosds
# ========================================================


# ========================================================
# --- SEKARANG ANDA BISA MENGGUNAKAN IMPORT DARI ROVOSDS ---
# ========================================================
from rovosds.domain import DomainParticipant
from rovosds.idl import IdlStruct
from rovosds.topic import Topic
from rovosds.sub import Subscriber as DDSSubscriber, DataReader
from rovosds.pub import Publisher as DDSPublisher, DataWriter
