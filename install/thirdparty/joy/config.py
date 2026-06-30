    # def create_joystick_buttons(self):
    #     """
    #     CONTOH INPUT DATA DARI COREL DRAW (0,0 DI TENGAH):
    #     Masukkan ukuran tombol (target_w_mm & target_h_mm) sesuai ukuran aslinya di Corel agar proporsional.
    #     """

    #     self.place_corel_center_element(
    #         filename="kotak.png",
    #         name="btn_square",
    #         corel_x_mm=48.678,    # <--- Nilai Negatif dari Corel aman digunakan!
    #         corel_y_mm=28.163,     # Nilai Y positif (agak ke atas dari center)
    #         target_w_mm=12.615,    # Ukuran lebar tombol dalam mm di Corel
    #         target_h_mm=12.615,    # Ukuran tinggi tombol dalam mm di Corel
    #         is_button=True,
    #         command=lambda: self.on_button_click("GRIP (Kotak)")
    #     )

    #     self.place_corel_center_element(
    #         filename="segitiga.png",
    #         name="btn_triangle",
    #         corel_x_mm=63.215,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=42.563,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=12.615,
    #         target_h_mm=12.615,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (Segitiga)")
    #     )

    #     self.place_corel_center_element(
    #         filename="x.png",
    #         name="btn_x",
    #         corel_x_mm=63.772,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=13.084,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=12.615,
    #         target_h_mm=12.615,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (X)")
    #     )

    #     self.place_corel_center_element(
    #         filename="bulat.png",
    #         name="btn_circle",
    #         corel_x_mm=78.143,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=28.187,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=12.615,
    #         target_h_mm=12.615,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (Bulat)")
    #     )

    #     self.place_corel_center_element(
    #         filename="r1.png",
    #         name="btn_r1",
    #         corel_x_mm=61.563,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=59.996,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=24.807,
    #         target_h_mm=5.08,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (R1)")
    #     )

    #     self.place_corel_center_element(
    #         filename="l1.png",
    #         name="btn_l1",
    #         corel_x_mm=-61.563,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=59.996,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=24.807,
    #         target_h_mm=5.08,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (L1)")
    #     )

    #     self.place_corel_center_element(
    #         filename="r2.png",
    #         name="btn_r2",
    #         corel_x_mm=61.406,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=71.451,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=24.687,
    #         target_h_mm=14.041,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (R2)")
    #     )

    #     self.place_corel_center_element(
    #         filename="l2.png",
    #         name="btn_l2",
    #         corel_x_mm=-61.406,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=71.451,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=24.687,
    #         target_h_mm=14.041,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (L2)")
    #     )

    #     self.place_corel_center_element(
    #         filename="analog.png",
    #         name="btn_analogR",
    #         corel_x_mm=31.993,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=0.502,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=16,
    #         target_h_mm=16,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (AR)")
    #     )

    #     self.place_corel_center_element(
    #         filename="analog.png",
    #         name="btn_analogL",
    #         corel_x_mm=-31.993,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=0.502,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=16,
    #         target_h_mm=16,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (AL)")
    #     )

    #     self.place_corel_center_element(
    #         filename="up.png",
    #         name="btn_up",
    #         corel_x_mm=-63.728,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=37.401,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=10.922,
    #         target_h_mm=13.208,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (Up)")
    #     )

    #     self.place_corel_center_element(
    #         filename="down.png",
    #         name="btn_down",
    #         corel_x_mm=-63.728,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=18.168,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=10.922,
    #         target_h_mm=13.208,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (down)")
    #     )

    #     self.place_corel_center_element(
    #         filename="r.png",
    #         name="btn_r",
    #         corel_x_mm=-54.379,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=27.784,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=13.123,
    #         target_h_mm=10.837,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (r)")
    #     )

    #     self.place_corel_center_element(
    #         filename="l.png",
    #         name="btn_l",
    #         corel_x_mm=-73.223,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=27.784,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=13.123,
    #         target_h_mm=10.837,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (l)")
    #     )

    #     self.place_corel_center_element(
    #         filename="share.png",
    #         name="btn_option",
    #         corel_x_mm=41.983,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=47.879,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=6.943,
    #         target_h_mm=11.515,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (Opt)")
    #     )

    #     self.place_corel_center_element(
    #         filename="share.png",
    #         name="btn_share",
    #         corel_x_mm=-40.104,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=47.1,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=6.943,
    #         target_h_mm=11.515,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (Share)")
    #     )

    #     self.place_corel_center_element(
    #         filename="touch.png",
    #         name="btn_touch",
    #         corel_x_mm=0.0,     # Nilai Positf (Sebelah Kanan)
    #         corel_y_mm=39.248,     # Nilai Y positif (Lebih atas lagi)
    #         target_w_mm=66.379,
    #         target_h_mm=36.661,
    #         is_button=True,
    #         command=lambda: self.on_button_click("ROLL (Touchpad)")
    #     )

    # def on_button_click(self, button_name):
    #     print(f"[*] Tombol {button_name} ditekan!")