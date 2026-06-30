import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import os
import math
import yaml
from logic import MapperLogic
from reader import JoyReader  

class CorelCenterMapper:
    def __init__(self, root):
        self.root = root
        self.logic = MapperLogic()
        self.joystick = JoyReader()  
        
        self.selected_table_row = None
        self.active_tree = None
        self.active_category = None
        
        self.button_canvas_ids = {} 
        self.button_names_by_id = {}
        self.analog_centers = {} 
        self.is_dragging = False
        
        # Dictionary untuk menyimpan referensi gambar versi normal dan versi transparan (opasitas 0.5)
        self.normal_images = {}
        self.trans_images = {}

        self.root.title("AQUA ROV Joystick Mapper")
        self.root.configure(bg="#2c3e50")

        canvas_w_px = self.logic.mm_to_px(self.logic.canvas_width_mm)
        canvas_h_px = self.logic.mm_to_px(self.logic.canvas_height_mm)
        self.root.geometry(f"{canvas_w_px + 400}x{canvas_h_px + 100}")

        self.main_frame = tk.Frame(self.root, bg="#2c3e50")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.left_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.left_frame.pack(side="left", fill="both", expand=True)

        self.btn_save_as = tk.Button(
            self.left_frame, # <-- Diubah dari root ke self.right_frame
            text="Save As", 
            command=self.save_as_config,
            font=("Arial", 14, "bold"), 
            padx=15, 
            pady=8
        )
        # Di-pack pertama kali di right_frame agar posisinya paling atas di sebelah kanan
        self.btn_save_as.pack(side=tk.TOP, anchor=tk.NW, pady=(0, 15))

        self.canvas = tk.Canvas(self.left_frame, width=canvas_w_px, height=canvas_h_px, bg="#eeeeee", highlightthickness=0)
        self.canvas.pack()
        
        self.right_frame = tk.Frame(self.main_frame, bg="#2c3e50")
        self.right_frame.pack(side="right", fill="both", padx=(20, 0))

        self.setup_tablemove()
        self.setup_tablegrip()
        self.setup_tablemode()
        
        self.populate_table()

        # Inisialisasi gambar transparan 0.5 di background
        self.load_background_image()

        # Masukkan referensi gambar normal ke dictionary
        self.image_references = self.normal_images

        self.create_joystick_buttons()
        
        # Mulai loop pengecekan stik fisik
        self.check_physical_joystick()

    def load_background_image(self):
        full_path = self.logic.get_full_path("stikbase.png")
        if not os.path.exists(full_path): return

        img = Image.open(full_path)
        img_resized = img.resize((
            self.logic.mm_to_px(200.067), 
            self.logic.mm_to_px(122.682)
        ), Image.Resampling.LANCZOS)
        
        tk_img = ImageTk.PhotoImage(img_resized)
        self.base_image_ref = tk_img # Simpan referensi agar tidak terhapus garbage collection
        
        cx_px, cy_px = self.logic.corel_to_tk_px(0.0, -1.362)
        self.canvas.create_image(cx_px, cy_px, image=tk_img)

    def setup_tablemove(self):
        lbl_table = tk.Label(self.right_frame, text="MOVEMENT", font=("Helvetica", 11, "bold"), bg="#2c3e50", fg="#ecf0f1")
        lbl_table.pack(anchor="w", pady=(2, 2))
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#1abc9c", foreground="white", font=("Helvetica", 9, "bold"))
        style.configure("Treeview", background="#34495e", fieldbackground="#34495e", foreground="white", rowheight=24, font=("Helvetica", 10))
        style.map("Treeview", background=[("selected", "#2ecc71")], foreground=[("selected", "white")])
        
        table_container = tk.Frame(self.right_frame, bg="#2c3e50")
        table_container.pack(fill="x", anchor="n")

        self.tree_move = ttk.Treeview(table_container, columns=("Button Name", "Function"), show="headings", height=13)
        self.tree_move.heading("Button Name", text="Button Name")
        self.tree_move.heading("Function", text="Function")
        self.tree_move.column("Button Name", width=120, anchor="center")
        self.tree_move.column("Function", width=180, anchor="center")
        self.tree_move.pack(fill="both")
        self.tree_move.bind("<<TreeviewSelect>>", lambda event: self.on_row_select(self.tree_move, "movement"))
        
        # Konfigurasi tag highlight warna kuning
        self.tree_move.tag_configure("highlight", background="#f1c40f", foreground="black")

    def setup_tablegrip(self):
        lbl_table = tk.Label(self.right_frame, text="GRIPPER", font=("Helvetica", 11, "bold"), bg="#2c3e50", fg="#ecf0f1")
        lbl_table.pack(anchor="w", pady=(8, 2))
        table_container = tk.Frame(self.right_frame, bg="#2c3e50")
        table_container.pack(fill="x", anchor="n")

        self.tree_grip = ttk.Treeview(table_container, columns=("Button Name", "Function"), show="headings", height=3)
        self.tree_grip.heading("Button Name", text="Button Name")
        self.tree_grip.heading("Function", text="Function")
        self.tree_grip.column("Button Name", width=120, anchor="center")
        self.tree_grip.column("Function", width=180, anchor="center")
        self.tree_grip.pack(fill="both")
        self.tree_grip.bind("<<TreeviewSelect>>", lambda event: self.on_row_select(self.tree_grip, "gripper"))
        self.tree_grip.tag_configure("highlight", background="#f1c40f", foreground="black")

    def setup_tablemode(self):
        lbl_table = tk.Label(self.right_frame, text="MODE", font=("Helvetica", 11, "bold"), bg="#2c3e50", fg="#ecf0f1")
        lbl_table.pack(anchor="w", pady=(8, 2))
        table_container = tk.Frame(self.right_frame, bg="#2c3e50")
        table_container.pack(fill="x", anchor="n")

        self.tree_mode = ttk.Treeview(table_container, columns=("Button Name", "Function"), show="headings", height=4)
        self.tree_mode.heading("Button Name", text="Button Name")
        self.tree_mode.heading("Function", text="Function")
        self.tree_mode.column("Button Name", width=120, anchor="center")
        self.tree_mode.column("Function", width=180, anchor="center")
        self.tree_mode.pack(fill="both")
        self.tree_mode.bind("<<TreeviewSelect>>", lambda event: self.on_row_select(self.tree_mode, "mode"))
        self.tree_mode.tag_configure("highlight", background="#f1c40f", foreground="black")

    def populate_table(self):
        for tree in [self.tree_move, self.tree_grip, self.tree_mode]:
            for item in tree.get_children():
                tree.delete(item)
            
        for cat, tree_widget in [("movement", self.tree_move), ("gripper", self.tree_grip), ("mode", self.tree_mode)]:
            if cat in self.logic.mappings and isinstance(self.logic.mappings[cat], dict):
                for func, code in self.logic.mappings[cat].items():
                    display_name = self.logic.code_to_btn.get(code, code)
                    tree_widget.insert("", "end", values=(display_name, func))

    def on_row_select(self, tree_widget, category):
        for tree in [self.tree_move, self.tree_grip, self.tree_mode]:
            if tree != tree_widget:
                tree.selection_remove(tree.selection())
        selected = tree_widget.selection()
        if selected:
            self.selected_table_row = selected[0]
            self.active_tree = tree_widget
            self.active_category = category

    def on_canvas_button_click(self, canvas_id):
        if not self.selected_table_row or not self.active_tree or not self.active_category:
            return
        clicked_btn_name = self.button_names_by_id.get(canvas_id)
        if not clicked_btn_name or clicked_btn_name in ["AL", "AR"]:
            return

        code_name = self.logic.btn_to_code.get(clicked_btn_name, clicked_btn_name)
        
        # Efek visual berkedip (tetap pakai state hidden untuk klik mouse)
        self.canvas.itemconfig(canvas_id, state="hidden")
        self.root.after(150, lambda: self.canvas.itemconfig(canvas_id, state="normal"))

        func_name = self.active_tree.item(self.selected_table_row, "values")[1]
        self.logic.update_mapping(self.active_category, func_name, code_name)
        self.populate_table()
        # generate_joy_map()
        self.reset_selection()

    def on_analog_drag(self, event, canvas_id, btn_name):
        self.is_dragging = True # <--- Kunci agar fungsi background tahu mouse lagi dipakai
        orig_x, orig_y = self.analog_centers[canvas_id]
        dx = event.x - orig_x
        dy = event.y - orig_y
        distance = math.sqrt(dx**2 + dy**2)
        
        max_limit = 15 
        if distance > max_limit:
            angle = math.atan2(dy, dx)
            new_x = orig_x + max_limit * math.cos(angle)
            new_y = orig_y + max_limit * math.sin(angle)
        else:
            new_x = event.x
            new_y = event.y
            
        self.canvas.coords(canvas_id, new_x, new_y)

    def on_analog_release(self, event, canvas_id, btn_name):
        self.is_dragging = False
        orig_x, orig_y = self.analog_centers[canvas_id]
        curr_x, curr_y = self.canvas.coords(canvas_id)
        
        dx = curr_x - orig_x
        dy = curr_y - orig_y
        distance = math.sqrt(dx**2 + dy**2)
        
        self.canvas.coords(canvas_id, orig_x, orig_y)
        
        if self.selected_table_row and self.active_tree and self.active_category:
            func_name = self.active_tree.item(self.selected_table_row, "values")[1]
            
            if distance <= 5:
                final_code = "b13" if btn_name == "AL" else "b14"
            else:
                base_x = "a0" if btn_name == "AL" else "a2"
                base_y = "a1" if btn_name == "AL" else "a3"
                
                if abs(dx) > abs(dy):
                    final_code = f"{base_x}(1)" if dx > 0 else f"{base_x}(-1)"
                else:
                    final_code = f"{base_y}(1)" if dy < 0 else f"{base_y}(-1)"
            
            self.logic.update_mapping(self.active_category, func_name, final_code)
            self.populate_table()
            # generate_joy_map()
            self.reset_selection()

    def check_physical_joystick(self):
        active_inputs = self.joystick.get_active_inputs()
        
        # Reset tag highlight kuning di semua tabel
        for tree in [self.tree_move, self.tree_grip, self.tree_mode]:
            for item in tree.get_children():
                tree.item(item, tags=())

        # Reset semua gambar tombol canvas ke versi NORMAL saat tidak ditekan
        for btn_id in self.button_names_by_id.keys():
            name = self.button_names_by_id[btn_id]
            if name not in ["AL", "AR"] and name in self.normal_images:
                # Tukar kembali ke gambar normal (opasitas 1.0)
                self.canvas.itemconfig(btn_id, image=self.normal_images[name])

        # === BAGIAN DUPLIKASI ANALOG DI ATAS SUDAH DIHAPUS ===

        # Jika ada input aktif dari stik fisik
        if active_inputs:
            for inp in active_inputs:
                # 1. Highlight Tabel Kuning
                for tree in [self.tree_move, self.tree_grip, self.tree_mode]:
                    for item in tree.get_children():
                        val = tree.item(item, "values")
                        if val and val[0] == self.logic.code_to_btn.get(inp, inp):
                            tree.item(item, tags=("highlight",))

                # 2. Efek Transparan 0.5 pada Tombol Canvas
                btn_human_name = self.logic.code_to_btn.get(inp, None)
                if btn_human_name and btn_human_name in self.button_canvas_ids:
                    b_id = self.button_canvas_ids[btn_human_name]
                    if btn_human_name not in ["AL", "AR"] and btn_human_name in self.trans_images:
                        self.canvas.itemconfig(b_id, image=self.trans_images[btn_human_name])

            # 3. Logika Remapping & Auto-generate joy_map.yaml
            if self.selected_table_row and self.active_tree and self.active_category:
                input_terpilih = active_inputs[0]
                func_name = self.active_tree.item(self.selected_table_row, "values")[1]
                self.logic.update_mapping(self.active_category, func_name, input_terpilih)
                self.populate_table()
                # generate_joy_map() # <--- Panggil konverter yaml otomatis disini
                self.reset_selection()

        # Update pergerakan analog HANYA JIKA mouse tidak sedang melakukan drag
        if not self.is_dragging:
            # Pergerakan Analog AL
            al_id = self.button_canvas_ids.get("AL")
            if al_id:
                ax = self.joystick.joy_axis.get("a0", 0.0)
                ay = self.joystick.joy_axis.get("a1", 0.0)
                ox, oy = self.analog_centers[al_id]
                self.canvas.coords(al_id, ox + (ax * 15), oy + (ay * 15))

            # Pergerakan Analog AR
            ar_id = self.button_canvas_ids.get("AR")
            if ar_id:
                ax = self.joystick.joy_axis.get("a2", 0.0)
                ay = self.joystick.joy_axis.get("a3", 0.0)
                ox, oy = self.analog_centers[ar_id]
                self.canvas.coords(ar_id, ox + (ax * 15), oy + (ay * 15))

        # Loop ulang fungsi check setiap 30 milidetik
        self.root.after(30, self.check_physical_joystick)

    def reset_selection(self):
        self.selected_table_row = None
        self.active_tree = None
        self.active_category = None

    def place_corel_center_element(self, filename, name, corel_x_mm, corel_y_mm, target_w_mm, target_h_mm, is_button=False, btn_name=None):
        full_path = self.logic.get_full_path(filename)
        if not os.path.exists(full_path): return None

        cx_px, cy_px = self.logic.corel_to_tk_px(corel_x_mm, corel_y_mm)
        tw_px = self.logic.mm_to_px(target_w_mm)
        th_px = self.logic.mm_to_px(target_h_mm)

        # Muat gambar asli dengan PIL
        img = Image.open(full_path)
        img_resized = img.resize((tw_px, th_px), Image.Resampling.LANCZOS)
        
        # 1. Simpan versi NORMAL (opasitas 1.0)
        tk_img_normal = ImageTk.PhotoImage(img_resized)
        if is_button:
            self.normal_images[btn_name] = tk_img_normal

        # 2. PROSES VERSI TRANSPARAN 0.5 (Jika gambar memiliki channel Alpha/RGBA)
        if is_button and btn_name not in ["AL", "AR"] and img_resized.mode == "RGBA":
            # Pisahkan channel Alpha
            alpha = img_resized.split()[3]
            # Kalikan Alpha dengan 0.5 (tingkat opasitas 50%)
            alpha = alpha.point(lambda p: int(p * 0.5))
            # Pasang kembali Alpha yang sudah dikurangi ke gambar asli
            img_resized.putalpha(alpha)
            # Simpan versi TRANSPARAN
            tk_img_trans = ImageTk.PhotoImage(img_resized)
            self.trans_images[btn_name] = tk_img_trans
        else:
            # AL, AR, stikbase, atau gambar non-RGBA tidak dibuatkan versi transparan
            pass

        # === BUAT ELEMEN CANVAS MENGGUNAKAN GAMBAR NORMAL AWAL ===
        if is_button:
            # Gunakan versi normal sebagai gambar default di canvas
            btn_image_id = self.canvas.create_image(cx_px, cy_px, image=tk_img_normal)
            self.button_canvas_ids[btn_name] = btn_image_id
            self.button_names_by_id[btn_image_id] = btn_name

            self.canvas.tag_bind(btn_image_id, "<Enter>", lambda e: self.canvas.config(cursor="hand2"))
            self.canvas.tag_bind(btn_image_id, "<Leave>", lambda e: self.canvas.config(cursor=""))
            
            if btn_name in ["AL", "AR"]:
                self.analog_centers[btn_image_id] = (cx_px, cy_px)
                self.canvas.tag_bind(btn_image_id, "<B1-Motion>", lambda event, b_id=btn_image_id, name=btn_name: self.on_analog_drag(event, b_id, name))
                self.canvas.tag_bind(btn_image_id, "<ButtonRelease-1>", lambda event, b_id=btn_image_id, name=btn_name: self.on_analog_release(event, b_id, name))
            else:
                self.canvas.tag_bind(btn_image_id, "<Button-1>", lambda event, b_id=btn_image_id: self.on_canvas_button_click(b_id))
            return btn_image_id
        else:
            # stikbase menggunakan gambar PIL langsung yang dikonversi di load_background_image
            pass

    def create_joystick_buttons(self):
        # ... (Parameter coordinate tombol tetap sama)
        self.place_corel_center_element("kotak.png", "btn_square", 48.678, 28.163, 12.615, 12.615, is_button=True, btn_name="Kotak")
        self.place_corel_center_element("segitiga.png", "btn_triangle", 63.215, 42.563, 12.615, 12.615, is_button=True, btn_name="Segitiga")
        self.place_corel_center_element("x.png", "btn_x", 63.772, 13.084, 12.615, 12.615, is_button=True, btn_name="X")
        self.place_corel_center_element("bulat.png", "btn_circle", 78.143, 28.187, 12.615, 12.615, is_button=True, btn_name="Bulat")
        self.place_corel_center_element("r1.png", "btn_r1", 61.563, 59.996, 24.807, 5.08, is_button=True, btn_name="R1")
        self.place_corel_center_element("l1.png", "btn_l1", -61.563, 59.996, 24.807, 5.08, is_button=True, btn_name="L1")
        self.place_corel_center_element("r2.png", "btn_r2", 61.406, 71.451, 24.687, 14.041, is_button=True, btn_name="R2")
        self.place_corel_center_element("l2.png", "btn_l2", -61.406, 71.451, 24.687, 14.041, is_button=True, btn_name="L2")
        self.place_corel_center_element("analog.png", "btn_analogR", 31.993, 0.502, 16, 16, is_button=True, btn_name="AR")
        self.place_corel_center_element("analog.png", "btn_analogL", -31.993, 0.502, 16, 16, is_button=True, btn_name="AL")
        self.place_corel_center_element("up.png", "btn_up", -63.728, 37.401, 10.922, 13.208, is_button=True, btn_name="Dpad_Up")
        self.place_corel_center_element("down.png", "btn_down", -63.728, 18.168, 10.922, 13.208, is_button=True, btn_name="Dpad_Down")
        self.place_corel_center_element("r.png", "btn_r", -54.379, 27.784, 13.123, 10.837, is_button=True, btn_name="Dpad_Right")
        self.place_corel_center_element("l.png", "btn_l", -73.223, 27.784, 13.123, 10.837, is_button=True, btn_name="Dpad_Left")
        self.place_corel_center_element("share.png", "btn_option", 41.983, 47.879, 6.943, 11.515, is_button=True, btn_name="Option")
        self.place_corel_center_element("share.png", "btn_share", -40.104, 47.1, 6.943, 11.515, is_button=True, btn_name="Share")
        self.place_corel_center_element("touch.png", "btn_touch", 0.0, 39.248, 66.379, 36.661, is_button=True, btn_name="Touchpad")

    def save_as_config(self):
        """Fungsi baru untuk Save As (menentukan direktori & nama file sendiri)"""
        current_dir = os.path.dirname(os.path.abspath(__file__))
        con_path = os.path.join(current_dir, "config", "mapping.yaml")

        target_path = filedialog.asksaveasfilename(
            initialdir=os.path.dirname(con_path),
            title="Simpan Konfigurasi Sebagai",
            defaultextension=".yaml",
            filetypes=[("YAML Files", "*.yaml"), ("All Files", "*.*")]
        )

        # root.destroy()

        generate_joy_map(target_path)

def generate_joy_map(target_path):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    mapping_path = os.path.join(current_dir, "config", "mapping.yaml")

    joy_map_path = target_path
    
    if not os.path.exists(mapping_path):
        return

    # 1. Baca data dari mapping.yaml asli milikmu
    with open(mapping_path, "r") as f:
        src = yaml.safe_load(f) or {}

    move = src.get("movement", {})
    grip = src.get("gripper", {})
    mode = src.get("mode", {})

    # Helper untuk membersihkan tanda kurung, misal "a1(1)" -> "a1"
    def clean(code):
        if not code: return ""
        return str(code).split("(")[0] if "(" in str(code) else str(code)

    # Helper untuk menggabungkan dua tombol berpasangan menjadi "pos,neg"
    def pair(pos_key, neg_key):
        p = clean(move.get(pos_key, ""))
        n = clean(move.get(neg_key, ""))
        if p and n: return f"{p},{n}"
        return p or n

    # 2. Strukturisasi ulang data sesuai target konfigurasi ROVOS2
    joy_map_data = {
        "key_mapping": {
            "lin_x": clean(move.get("Geser Kanan", move.get("Geser Kiri", ""))),
            "lin_y": clean(move.get("Maju", move.get("Mundur", ""))),
            "lin_z": pair("Kedalaman Up", "Kedalaman Down"),
            "ang_x": clean(move.get("Roll Kanan", move.get("Roll Kiri", ""))),
            "ang_y": clean(move.get("Pitch Depan", move.get("Pitch Belakang", ""))),
            "ang_z": pair("Belok Kanan", "Belok Kiri")  # Hasilnya: "b10,b9"
        },
        "axis_invert": src.get("axis_invert", {
            "a0": "1", "a1": "-1", "a2": "1", "a3": "-1", "a4": "1", "a5": "1"
        }),
        "gripper_mapping": {
            "grip": clean(grip.get("Griper Open/Close", "")),
            "roll": clean(grip.get("Griper Roll", "")),
            "pitch": clean(grip.get("Griper Pitch", ""))
        },
        "mode_mapping": {
            "auto": clean(mode.get("Mode Switch", "")),
            "depthlock": clean(mode.get("Deepth Lock", "")),
            "rotationlock": clean(mode.get("Rotation Lock", "")),
            "emergency": clean(mode.get("Emergency", ""))
        }
    }

    # 3. Simpan hasil reconfig ke joy_map.yaml dengan format rapi
    os.makedirs(os.path.dirname(joy_map_path), exist_ok=True)
    with open(joy_map_path, "w") as f:
        f.write("# CONFIGURATION: KEY MAPPING\n")
        yaml.dump({"key_mapping": joy_map_data["key_mapping"]}, f, default_flow_style=False)
        
        f.write("\n# CONFIGURATION: AXIS INVERSION\n")
        yaml.dump({"axis_invert": joy_map_data["axis_invert"]}, f, default_flow_style=False)
        
        f.write("\n# CONFIGURATION: GRIPPER MAPPING\n")
        yaml.dump({"gripper_mapping": joy_map_data["gripper_mapping"]}, f, default_flow_style=False)
        
        f.write("\n# CONFIGURATION: MODE MAPPING\n")
        yaml.dump({"mode_mapping": joy_map_data["mode_mapping"]}, f, default_flow_style=False)
        
if __name__ == "__main__":
    root = tk.Tk()
    app = CorelCenterMapper(root)
    root.mainloop()