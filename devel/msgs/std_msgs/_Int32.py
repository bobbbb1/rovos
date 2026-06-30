from msg_struct import IdlStruct

class Int32(IdlStruct):
    data: int

    def __init__(self, data: int = 0):
        super().__init__()
        self.data = int(data)
