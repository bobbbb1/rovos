from msg_struct import IdlStruct, sequence

class Image(IdlStruct):
    timestamp: float

    height: int
    width: int

    encoding: str

    is_bigendian: int

    step: int

    data: sequence[int]

    def __init__(
        self, 
        timestamp: float = 0.0, 
        height: int = 0, 
        width: int = 0, 
        encoding: str = "rgb8", 
        is_bigendian: int = 0, 
        step: int = 0, 
        data: list = None
    ):
        super().__init__()
        self.timestamp = float(timestamp)
        self.height = int(height)
        self.width = int(width)
        self.encoding = str(encoding)
        self.is_bigendian = int(is_bigendian)
        self.step = int(step)
        self.data = list(data) if data is not None else []
