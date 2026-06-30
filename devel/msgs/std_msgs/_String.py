from msg_struct import IdlStruct

class String(IdlStruct):
    data: str

    def __init__(self, data: str = ""):
        super().__init__()
        self.data = str(data)