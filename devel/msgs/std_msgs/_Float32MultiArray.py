from msg_struct import IdlStruct, sequence

class Float32MultiArray(IdlStruct):
    data: sequence[float]

    def __init__(self, data: list = None):
        super().__init__()
        self.data = list(data) if data is not None else []