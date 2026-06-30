import os

def generate_msg_classes(pkg_path, devel_path, silent=False):
    """
    Generator Pesan ROVOS2 - Spesifik untuk CycloneDDS IdlStruct
    """
    msg_dir = os.path.join(pkg_path, "msg")
    if not os.path.exists(msg_dir):
        return

    pkg_name = os.path.basename(pkg_path)
    target_pkg_name = f"{pkg_name}_msgs" if not pkg_name.endswith("_msgs") else pkg_name
    
    target_msg_dir = os.path.join(devel_path, "msgs", target_pkg_name)
    os.makedirs(target_msg_dir, exist_ok=True)

    generated_messages = []

    for file in os.listdir(msg_dir):
        if file.endswith(".msg"):
            msg_name = file.replace(".msg", "")
            msg_file_path = os.path.join(msg_dir, file)
            
            file_py_name = f"_{msg_name}"
            target_py_path = os.path.join(target_msg_dir, f"{file_py_name}.py")

            if not silent:
                print(f"[\033[94mMSG\033[0m] [{pkg_name}] Generating DDS MSG: {file} -> msgs/{target_pkg_name}/{file_py_name}.py")

            properties = []
            imports_needed = set()
            
            # Selalu butuh IdlStruct untuk compiler CycloneDDS
            imports_needed.add("from msg_struct import IdlStruct")

            with open(msg_file_path, "r") as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith("#"):
                        parts = line.split()
                        if len(parts) >= 2:
                            type_msg, name_msg = parts[0], parts[1]
                            properties.append((type_msg, name_msg))
                            
                            # Jalur import sesuai request skema barumu
                            if type_msg == "Header":
                                imports_needed.add("from msg_struct import Header")
                            elif type_msg in ["Int32", "Float32MultiArray"]:
                                imports_needed.add(f"from std_msgs import {type_msg}")

            # Tulis file Python otomatis dengan gaya IdlStruct CycloneDDS
            with open(target_py_path, "w") as py_f:
                py_f.write("# Generated otomatis oleh ROVOS2 DDS Message Generator\n")
                
                if imports_needed:
                    for imp in sorted(imports_needed):
                        py_f.write(f"{imp}\n")
                py_f.write("\n")
                
                # Definisi Class sebagai IdlStruct
                py_f.write(f"class {msg_name}(IdlStruct):\n")
                
                # Bagian 1: Definisi Type Hinting (Wajib untuk CycloneDDS IDL)
                if not properties:
                    py_f.write("    pass\n")
                else:
                    for type_msg, name_msg in properties:
                        py_f.write(f"    {name_msg}: {type_msg}\n")
                    
                    # Bagian 2: Constructor __init__
                    py_f.write("\n    def __init__(self):\n")
                    py_f.write("        super().__init__()\n")
                    for type_msg, name_msg in properties:
                        py_f.write(f"        self.{name_msg} = {type_msg}()\n")
                
                # Bagian 3: Fungsi Serializer Khusus DDS (Aman dari internal dict bawaan DDS)
                py_f.write("\n    def to_json(self):\n")
                py_f.write("        import json\n")
                py_f.write("        def dds_encoder(obj):\n")
                py_f.write("            if hasattr(obj, '__dict__'):\n")
                # Menyaring field IDL asli agar tidak kemasukan variable sampah dari internal CycloneDDS
                py_f.write("                return {k: v for k, v in obj.__dict__.items() if not k.startswith('_')}\n")
                py_f.write("            return str(obj)\n")
                py_f.write("        return json.dumps({k: v for k, v in self.__dict__.items() if not k.startswith('_')}, default=dds_encoder)\n")
            
            generated_messages.append((file_py_name, msg_name))

    # 2. BUAT FILE __init__.py
    if generated_messages:
        init_path = os.path.join(target_msg_dir, "__init__.py")
        with open(init_path, "w") as init_f:
            init_f.write("# Generated otomatis oleh ROVOS2 untuk ekspos class ke PYTHONPATH\n")
            for file_py, class_name in generated_messages:
                init_f.write(f"from .{file_py} import {class_name}\n")