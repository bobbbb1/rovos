#!/usr/bin/env python3
import os
import sys
import re
import py_compile
import json
import subprocess
import shutil
import fnmatch
import xml.etree.ElementTree as ET

# =======================================================================
# [HARD PROTECTION: ENVIRONMENT VALIDATION]
# =======================================================================
if "ROVOS_WS_ACTIVE" not in os.environ:
    print("[\033[91mERROR\033[0m] Workspace Environment Not Activated!")
    print("-----------------------------------------------------------------------")
    sys.exit(1)
# =======================================================================
# [PATH CONFIGURATION] 
# =======================================================================
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
CLI_PATH = os.path.normpath(os.path.join(CUR_PATH, "..")) 
DEVEL_PATH = os.path.normpath(os.path.join(CLI_PATH, "..")) 

CORE_ROOT_PATH = os.path.normpath(os.path.join(DEVEL_PATH, "..")) 
CORE_DEVEL_PATH = os.path.join(CORE_ROOT_PATH, "devel")
CORE_INSTALL_PATH = os.path.join(CORE_ROOT_PATH, "install")

WS_PATH = os.getcwd() 
WS_SRC_PATH = os.path.join(WS_PATH, "src")
WS_DEVEL_PATH = os.path.join(WS_PATH, "devel")
WS_BUILD_PATH = os.path.join(WS_PATH, "build")

def build_workspace(silent=False):
    """Memeriksa syntax error di devel dan src, otomatis menduplikasi seluruh struktur devel/install dari core ke WS dengan filter .buildignore"""
    
    # 1. VALIDASI UTAMA: Folder 'src' di Root Workspace WAJIB ADA di awal!
    if not os.path.exists(WS_SRC_PATH) or not os.path.isdir(WS_SRC_PATH):
        print("[\033[91mERROR\033[0m] Gagal melakukan build! Folder '\033[93msrc\033[0m' tidak ditemukan di workspace ini.")
        print(f"        Pastikan Anda berada di direktori workspace yang benar: {WS_PATH}")
        sys.exit(1)

    if not silent:
        print(f"[\033[94mBUILD\033[0m] Target Workspace: {WS_PATH}")
        print("[\033[94mBUILD\033[0m] Started compiling package ROVOS2...")
    
    # ----------------------------------------------------------------------
    # 2. AUTOMATIC INITIALIZATION & COPY (DEVEL & INSTALL) DENGAN FILTER KETAT
    # ----------------------------------------------------------------------
    try:
        # --- MEMBACA .BUILDIGNORE DARI ROOT CORE ---
        buildignore_path = os.path.join(CORE_ROOT_PATH, ".buildignore")
        ignored_patterns = []
        
        if os.path.exists(buildignore_path):
            with open(buildignore_path, "r") as bi:
                for line in bi:
                    line = line.strip().replace('\\', '/')
                    # Lewati baris kosong atau komentar
                    if line and not line.startswith("#"):
                        # Jika baris adalah folder (ex: src atau devel/core), pastikan polanya mencakup isinya juga
                        ignored_patterns.append(line)
                        if not line.endswith("*"):
                            if line.endswith("/"):
                                ignored_patterns.append(line + "*")
                            else:
                                ignored_patterns.append(line + "/*")
        
        def should_ignore(rel_path):
            """Fungsi pembantu untuk mengecek apakah path relatif cocok dengan aturan .buildignore"""
            check_path = rel_path.replace('\\', '/')
            
            # Cek apakah path saat ini cocok dengan aturan di .buildignore
            for pattern in ignored_patterns:
                if fnmatch.fnmatch(check_path, pattern) or check_path == pattern:
                    return True
                    
            # Cek juga apakah ada folder induknya yang di-ignore
            parts = check_path.split('/')
            for i in range(1, len(parts)):
                parent_path = "/".join(parts[:i])
                if parent_path in ignored_patterns or (parent_path + "/*") in ignored_patterns:
                    return True
                    
            return False

        # --- PROSES COPY FOLDER/FILE DARI CORE KE WORKSPACE ---
        # Menyisir folder yang ada di Core untuk diduplikasi ke Workspace aktif
        for base_folder in ["devel", "install"]:
            core_base_dir = os.path.join(CORE_ROOT_PATH, base_folder)
            if not os.path.exists(core_base_dir):
                continue
                
            for root, dirs, files in os.walk(core_base_dir):
                # Ambil path relatif dari CORE_ROOT_PATH (misal: devel/core, install)
                rel_root = os.path.relpath(root, CORE_ROOT_PATH)
                
                # Jika folder induk masuk daftar ignore, lewati seluruh isinya!
                if should_ignore(rel_root):
                    continue
                    
                ws_target_dir = os.path.normpath(os.path.join(WS_PATH, rel_root))
                
                # Saring dan copy file di dalam folder tersebut
                for file in files:
                    rel_file_path = os.path.join(rel_root, file)
                    
                    if should_ignore(rel_file_path):
                        if not silent:
                            print(f"[\033[93mSKIP\033[0m] {rel_file_path}.")
                        continue

                    os.makedirs(ws_target_dir, exist_ok=True)
                        
                    full_core_file = os.path.join(CORE_ROOT_PATH, rel_file_path)
                    full_ws_file = os.path.join(WS_PATH, rel_file_path)
                    
                    # Salin file jika belum ada atau versi di core lebih baru
                    if not os.path.exists(full_ws_file) or os.path.getmtime(full_core_file) > os.path.getmtime(full_ws_file):
                        shutil.copy2(full_core_file, full_ws_file)

    except Exception as e:
        print(f"[\033[91mERROR\033[0m] Gagal menyalin komponen dari Core: {e}")
        sys.exit(1)

    # Buat folder build di sisi workspace
    os.makedirs(WS_BUILD_PATH, exist_ok=True)
    
    error_count = 0
    packages_found = {}

    # [PROSES 1: SCAN SYNTAX CORE YANG SUDAH DICOPY KE WORKSPACE]
    for folder_name in ["core", "rovos", "msgs"]:
        target_dir = os.path.normpath(os.path.join(WS_DEVEL_PATH, folder_name))
        if os.path.exists(target_dir):
            if not silent:
                print(f"[\033[90mSCAN\033[0m] checking folder devel/{folder_name}...")
            for root, _, files in os.walk(target_dir):
                for file in files:
                    if file.endswith(".py"):
                        full_path = os.path.join(root, file)
                        try:
                            py_compile.compile(full_path, doraise=True)
                        except py_compile.PyCompileError as e:
                            print(f"[\033[91mERROR\033[0m] Syntax error: {full_path}")
                            error_count += 1

    # [PROSES 2: SCAN USER PACKAGES - MURNI HANYA DI WS/SRC SEJAJAR DEVEL]
    if os.path.exists(WS_SRC_PATH):
        for pkg in os.listdir(WS_SRC_PATH):
            pkg_path = os.path.normpath(os.path.join(WS_SRC_PATH, pkg))
            
            if os.path.isdir(pkg_path):
                if not silent:
                    print(f"[\033[90mSCAN\033[0m] Found package: {pkg}")
                
                # Custom Message Generator (Output dilempar ke folder devel/msgs hasil copasan di Workspace)
                try:
                    generate_msg_classes(pkg_path, WS_DEVEL_PATH, silent=silent)
                except Exception as e:
                    print(f"[\033[91mERROR\033[0m] Failed to generate message from {pkg}: {e}")
                    error_count += 1
            
                # XML Auto-Dependencies
                xml_path = os.path.join(pkg_path, "package.xml")
                if os.path.exists(xml_path):
                    try:
                        tree = ET.parse(xml_path)
                        root_xml = tree.getroot()
                        dependencies = []
                        for tag in ['depend', 'exec_depend', 'build_depend']:
                            for dep in root_xml.findall(tag):
                                if dep.text:
                                    dependencies.append(dep.text.strip())
                        
                        for dep_name in dependencies:
                            if not silent:
                                print(f"[\033[90mDEPS\033[0m] Checking Dependency: {dep_name}...")
                            
                            # Menggunakan subprocess.run untuk menangkap stdout & stderr
                            result = subprocess.run(
                                [sys.executable, "-m", "pip", "install", dep_name],
                                capture_output=True,
                                text=True
                            )
                            
                            # Jika proses pip berhasil (returncode == 0)
                            if result.returncode == 0:

                                satisfied_packages = re.findall(
                                    r"Requirement already satisfied:\s*([a-zA-Z0-9_\-]+)", 
                                    result.stdout
                                )
                                
                                if satisfied_packages:

                                    for satisfied_pkg in sorted(set(satisfied_packages)):
                                        print(f"{satisfied_pkg} [\033[92mREADY\033[0m]")
                                else:

                                    print(f"{dep_name} [\033[92mINSTALLED\033[0m]")
                            else:

                                print(f"[\033[91mERROR\033[0m] Failed to install {dep_name}")
                                if not silent:
                                    print(result.stderr)
                                    
                    except Exception as e:
                        print(f"[\033[91mWARN\033[0m] Process Failed for {pkg} dependency: {e}")

                # Scan otomatis file .py di sub-folder paket internal user
                inner_pkg_path = os.path.join(pkg_path, pkg)
                if os.path.exists(inner_pkg_path):
                    for root, _, files in os.walk(inner_pkg_path):
                        for file in files:
                            if file.endswith(".py") and file != "__init__.py":
                                full_path = os.path.join(root, file)
                                try:
                                    py_compile.compile(full_path, doraise=True)
                                except py_compile.PyCompileError:
                                    print(f"[\033[91mERROR\033[0m] Syntax error in node: {file}")
                                    error_count += 1

                packages_found[pkg] = pkg_path

    # Tulis peta lokasi paket ke workspace_cache.json lokal milik Workspace
    with open(os.path.join(WS_BUILD_PATH, "workspace_cache.json"), "w") as f:
        json.dump(packages_found, f, indent=4)

    if not silent:
        if error_count == 0:
            print("[\033[92mSUCCESS\033[0m] Safe build! The 'build' folder was successfully generated.")
        else:
            print(f"[\033[91mFAILED\033[0m] Found {error_count} syntax error. Please check!")
            sys.exit(1)
            
    return error_count == 0

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
                            elif type_msg in ["Int32", "Float32", "Int32MultiArray", "Float32MultiArray", "String"]:
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