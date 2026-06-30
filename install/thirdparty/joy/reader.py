import time
import threading
import copy

class JoyReader():
    def __init__(self):
        self.device = None
        self.running = False

        self.PS4_VID = 0x054C  
        self.PS4_PID = 0x05C4

        self.joy_btn = {
            "b0": 0, "b1": 0, "b2": 0, "b3": 0, "b4": 0, "b5": 0, "b6": 0, "b7": 0, "b8": 0,
            "b9": 0, "b10": 0, "b11": 0, "b12": 0, "b13": 0, "b14": 0
        }
        self.joy_axis = {
            "a0": 0.0, "a1": 0.0, "a2": 0.0, "a3": 0.0, "a4": 0.0, "a5": 0.0
        }

        self.last_joy_btn = copy.deepcopy(self.joy_btn)
        self.last_joy_axis = copy.deepcopy(self.joy_axis)

        self.running = True
        self.worker_thread = threading.Thread(target=self.joyread_loop, daemon=True)
        self.worker_thread.start()

    def connect_usb(self):
        try:
            import hid
            self.device = hid.device()
            try:
                self.device.open(self.PS4_VID, 0x05C4)
            except IOError:
                self.device.open(self.PS4_VID, 0x09CC)
                
            self.device.set_nonblocking(True)
            print(f"\n[CONNECTED] USB Sukses! Stik PS4 aktif di backbone ROVOS2.\n")
            return True
        except Exception:
            print("<!> Mencari stik PS4 USB... Pastikan kabel sudah rapat.")
            return False

    def publish_joystick_state(self):
        pass

    def get_active_inputs(self):
        active = []
        
        for btn, val in self.joy_btn.items():
            if val == 1:
                active.append(btn)
                
        if self.joy_axis["a0"] >= 0.8: active.append("a0(1)")
        elif self.joy_axis["a0"] <= -0.8: active.append("a0(-1)")
        
        if self.joy_axis["a1"] <= -0.8: active.append("a1(1)")
        elif self.joy_axis["a1"] >= 0.8: active.append("a1(-1)")
        
        if self.joy_axis["a2"] >= 0.8: active.append("a2(1)")
        elif self.joy_axis["a2"] <= -0.8: active.append("a2(-1)")
        
        if self.joy_axis["a3"] <= -0.8: active.append("a3(1)")
        elif self.joy_axis["a3"] >= 0.8: active.append("a3(-1)")
        
        if self.joy_axis["a4"] >= 0.5: active.append("a4")
        if self.joy_axis["a5"] >= 0.5: active.append("a5")
        
        return active

    def joyread_loop(self):
        while self.running:
            if not self.device:
                if not self.connect_usb():
                    time.sleep(2)
                    continue

            try:
                report_terakhir = None

                while True:
                    report = self.device.read(64)
                    if not report: 
                        break  
                    report_terakhir = report  

                if report_terakhir:
                    report = report_terakhir
                    
                    raw_a0 = report[1]
                    raw_a1 = report[2]
                    raw_a2 = report[3]
                    raw_a3 = report[4]
                    raw_a4 = report[8]
                    raw_a5 = report[9]

                    an_x1 = round((raw_a0 - 128) / 128.0, 1)
                    an_y1 = round((raw_a1 - 128) / 128.0, 1)
                    an_x2 = round((raw_a2 - 128) / 128.0, 1)
                    an_y2 = round((raw_a3 - 128) / 128.0, 1)
                    tr_l2 = round(raw_a4 / 255.0, 1)
                    tr_r2 = round(raw_a5 / 255.0, 1)

                    self.joy_axis["a0"] = 0.0 if abs(an_x1) < 0.1 else an_x1
                    self.joy_axis["a1"] = 0.0 if abs(an_y1) < 0.1 else an_y1
                    self.joy_axis["a2"] = 0.0 if abs(an_x2) < 0.1 else an_x2
                    self.joy_axis["a3"] = 0.0 if abs(an_y2) < 0.1 else an_y2
                    self.joy_axis["a4"] = tr_l2
                    self.joy_axis["a5"] = tr_r2

                    byte5 = report[5]
                    byte6 = report[6]
                    byte7 = report[7]

                    self.joy_btn["b0"] = 1 if (byte5 & 0x20) else 0  
                    self.joy_btn["b1"] = 1 if (byte5 & 0x40) else 0  
                    self.joy_btn["b2"] = 1 if (byte5 & 0x10) else 0  
                    self.joy_btn["b3"] = 1 if (byte5 & 0x80) else 0  
                    self.joy_btn["b4"] = 1 if (byte7 & 0x02) else 0  

                    self.joy_btn["b9"] = 1 if (byte6 & 0x01) else 0  
                    self.joy_btn["b10"] = 1 if (byte6 & 0x02) else 0  
                    self.joy_btn["b11"] = 1 if (byte6 & 0x10) else 0  
                    self.joy_btn["b12"] = 1 if (byte6 & 0x20) else 0  
                    self.joy_btn["b13"] = 1 if (byte6 & 0x40) else 0  
                    self.joy_btn["b14"] = 1 if (byte6 & 0x80) else 0  

                    dpad = byte5 & 0x0F
                    self.joy_btn["b5"] = 1 if dpad in (0, 1, 7) else 0  
                    self.joy_btn["b6"] = 1 if dpad in (1, 2, 3) else 0  
                    self.joy_btn["b7"] = 1 if dpad in (3, 4, 5) else 0  
                    self.joy_btn["b8"] = 1 if dpad in (5, 6, 7) else 0  

                    if self.joy_axis != self.last_joy_axis or self.joy_btn != self.last_joy_btn:
                        self.publish_joystick_state()
                        self.last_joy_axis = copy.deepcopy(self.joy_axis)
                        self.last_joy_btn = copy.deepcopy(self.joy_btn)
                    
            except Exception as e:
                print(f"<!> Hubungan USB terputus atau gangguan data stik: {e}")
                self.device = None

            time.sleep(0.01)