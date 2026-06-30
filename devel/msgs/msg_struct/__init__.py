from cyclonedds.idl import IdlStruct
from cyclonedds.idl.types import sequence

class Time(IdlStruct):
    sec: int
    nanosec: int

    def __init__(self, sec: int = 0, nanosec: int = 0):
        super().__init__()
        self.sec = int(sec)
        self.nanosec = int(nanosec)

class Header(IdlStruct):
    stamp: Time
    frame_id: str

    def __init__(self, frame_id: str = ""):
        super().__init__()
        self.stamp = Time()
        self.frame_id = str(frame_id)