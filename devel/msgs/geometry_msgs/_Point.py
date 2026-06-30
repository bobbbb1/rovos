from msg_struct import IdlStruct

class Point(IdlStruct):
    x: float
    y: float
    z: float

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        super().__init__()
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)
