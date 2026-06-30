from msg_struct import IdlStruct

class Vector3(IdlStruct):
    x: float
    y: float
    z: float
    
    # SUNTIKAN AMAN: Menerima argumen apa pun dari internal .take() CycloneDDS
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Jika CycloneDDS memasukkan data lewat keyword arguments (kwargs)
        self.x = float(kwargs.get('x', args[0] if len(args) > 0 else 0.0))
        self.y = float(kwargs.get('y', args[1] if len(args) > 1 else 0.0))
        self.z = float(kwargs.get('z', args[2] if len(args) > 2 else 0.0))

class Twist(IdlStruct):
    linear: Vector3
    angular: Vector3
    
    # SUNTIKAN AMAN: Menerima argumen apa pun dari internal .take() CycloneDDS
    def __init__(self, *args, **kwargs):
        super().__init__()
        # Jika dikirim dari network, isi propertinya, jika tidak, buat objek Vector3 kosong
        self.linear = kwargs.get('linear', args[0] if len(args) > 0 else Vector3())
        self.angular = kwargs.get('angular', args[1] if len(args) > 1 else Vector3())