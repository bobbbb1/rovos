from msg_struct import IdlStruct, Header

class Point(IdlStruct):
    x: float
    y: float
    z: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
        
class PointStamped(IdlStruct):
    header: Header
    point: Point

    def __init__(self, frame_id: str = ""):
        super().__init__()
        self.header = Header(frame_id=frame_id)
        self.point = Point()
