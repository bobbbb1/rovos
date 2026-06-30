from msg_struct import IdlStruct, sequence

class Int32MultiArray(IdlStruct):
    data: sequence[int]

    def __init__(self, data: list = None):
        super().__init__()
        self.data = list(data) if data is not None else []
