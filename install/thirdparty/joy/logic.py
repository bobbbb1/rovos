import os
import sys
import yaml

class MapperLogic:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(sys.argv[0]))
        self.dpi_ratio = 96 / 26.4
        self.canvas_width_mm = 210.0
        self.canvas_height_mm = 170.0
        self.offset_x_mm = self.canvas_width_mm / 2.0
        self.offset_y_mm = self.canvas_height_mm / 2.0
        self.config_path = os.path.join(self.base_dir, "config", "mapping.yaml")
        self.joy_remap_path = os.path.join(self.base_dir, "config", "joy_map.yaml")
        
        self.btn_to_code = {
            "X": "b0", "Bulat": "b1", "Kotak": "b2", "Segitiga": "b3",
            "Touchpad": "b4", "Dpad_Up": "b5", "Dpad_Right": "b6", "Dpad_Down": "b7", "Dpad_Left": "b8",
            "L1": "b9", "R1": "b10", "Share": "b11", "Option": "b12",
            "L3": "b13", "R3": "b14", "L2": "a4", "R2": "a5"
        }
        self.code_to_btn = {v: k for k, v in self.btn_to_code.items()}

        self.mappings = self.load_mapping_config()

    def corel_to_tk_px(self, corel_x_mm, corel_y_mm):
        tk_x_mm = corel_x_mm + self.offset_x_mm
        tk_y_mm = self.offset_y_mm - corel_y_mm
        return int(tk_x_mm * self.dpi_ratio), int(tk_y_mm * self.dpi_ratio)

    def mm_to_px(self, value_mm):
        return int(value_mm * self.dpi_ratio)

    def get_full_path(self, filename):
        return os.path.join(self.base_dir, "img", filename)

    def load_mapping_config(self):
        if not os.path.exists(self.config_path):
            return {}
        try:
            with open(self.config_path, "r") as file:
                return yaml.safe_load(file) or {}
        except Exception:
            return {}

    def save_mapping_config(self):
        os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
        try:
            with open(self.config_path, "w") as file:
                yaml.safe_dump(self.mappings, file, default_flow_style=False, sort_keys=False, allow_unicode=True)
        except Exception as e:
            print(f"[!] Gagal menyimpan file YAML: {e}")

    def update_mapping(self, category, target_function, raw_code):
        for cat in ["movement", "gripper", "mode"]:
            if cat in self.mappings and isinstance(self.mappings[cat], dict):
                for func, code in self.mappings[cat].items():
                    if str(code) == str(raw_code) and not (cat == category and func == target_function):
                        self.mappings[cat][func] = '-'
        
        if category in self.mappings and target_function in self.mappings[category]:
            self.mappings[category][target_function] = raw_code
            
        self.save_mapping_config()

    def save_as_mapping_config(self, target_path):
        # Jika user memilih lokasi dan tidak menekan 'Cancel'
        if target_path:
            try:
                # Pastikan folder tujuan ada jika user mengetik folder baru
                os.makedirs(os.path.dirname(target_path), exist_ok=True)
                
                # Baca data dari joy_map.yaml
                with open(self.joy_remap_path, "r") as file_sumber:
                    data_joy = yaml.safe_load(file_sumber) or {}

                # Tulis data tersebut ke file baru yang ditargetkan
                with open(target_path, "w") as file_baru:
                    yaml.safe_dump(data_joy, file_baru, default_flow_style=False, sort_keys=False, allow_unicode=True)
                
                print(f"[*] Berhasil menyimpan konfigurasi ke: {target_path}")
                return True
            except Exception as e:
                print(f"[!] Gagal melakukan Save As: {e}")
                return False
        else:
            print("[*] Save As dibatalkan oleh pengguna.")
            return False