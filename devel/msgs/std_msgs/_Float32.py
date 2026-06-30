from msg_struct import IdlStruct

class Float32(IdlStruct):
    data: float

    def __init__(self, data: float = 0.0):
        super().__init__()
        self.data = float(data)