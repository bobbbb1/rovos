#!/usr/bin/env python3
import os
import sys
import json
import textwrap

# =======================================================================
# [PATH CONFIGURATION] 
# =======================================================================
CUR_PATH = os.path.dirname(os.path.abspath(__file__))
CLI_PATH = os.path.normpath(os.path.join(CUR_PATH, "..")) 
DEVEL_PATH = os.path.normpath(os.path.join(CLI_PATH, "..")) 

CORE_ROOT_PATH = os.path.normpath(os.path.join(DEVEL_PATH, "..")) 
CORE_DEVEL_PATH = os.path.join(CORE_ROOT_PATH, "devel")
CORE_INSTALL_PATH = os.path.join(CORE_ROOT_PATH, "install")

# List target dinamis
pkg_upd_list = ["thirdparty"]

def update_package(silent=False):
    for item in pkg_upd_list:
        core_path_target = os.path.join(CORE_INSTALL_PATH, item)

        if not os.path.exists(core_path_target) or not os.path.isdir(core_path_target):
            print(f"[\033[91mERROR\033[0m] Gagal melakukan update! Folder '\033[93m{item}\033[0m' tidak ditemukan.")
            sys.exit(1)

    if not silent:
        print("[\033[94mUPDATE\033[0m] Started update package ROVOS...")

    try:
        for update_item in pkg_upd_list:
            target_dir = os.path.join(CORE_INSTALL_PATH, update_item)
            update_package_json(target_dir, silent=silent)
            regen_setup_ps1(target_dir, silent=silent)

    except Exception as e:
        print(f"[\033[91mERROR\033[0m] Terjadi kegagalan proses update: {e}", file=sys.stderr)
        sys.exit(1)

def regen_setup_ps1(target_path, silent=False):
    target_check_dir = target_path
    if not os.path.exists(target_check_dir):
        return
    
    path_name = os.path.basename(target_check_dir) # e.g., "thirdparty"
    
    setup_name = f"setup_{path_name}.ps1"
    target_setup_file = os.path.join(CORE_INSTALL_PATH, setup_name)

    json_name = "package.json"
    # PERBAIKAN: Gunakan target_check_dir (path absolut)
    target_check_json = os.path.join(target_check_dir, json_name)

    if os.path.exists(target_check_json):
        with open(target_check_json, "r", encoding="utf-8") as jsonfile:
            data = json.load(jsonfile)

        packages = data.get("packages", [])

        ps_functions = []
        for pkg in packages:
            pkg_name = pkg.get("name")
            cli_name = pkg.get("cli")
            
            if pkg_name and cli_name:
                template = textwrap.dedent(f'''\
                    function {cli_name} {{
                        if (Test-Path "$env:ROVOS_CORE\\install\\{path_name}\\{pkg_name}\\main.py") {{
                            python "$env:ROVOS_CORE\\install\\{path_name}\\{pkg_name}\\main.py" $args
                        }} else {{
                            python "$env:ROVOS_CORE\\install\\{path_name}\\{pkg_name}\\main" $args
                        }}
                    }}''')
                ps_functions.append(template)

        full_content = "\n\n".join(ps_functions)

        with open(target_setup_file, "w", encoding="utf-8") as file:
            file.write(full_content + "\n")

        if not silent:
            print(f"[\033[94mINFO\033[0m] Successfully regenerated with {len(packages)} functions.")

def update_package_json(target_path, silent=False):
    target_check_dir = target_path
    if not os.path.exists(target_check_dir):
        return

    json_name = "package.json"
    target_check_json = os.path.join(target_path, json_name)

    package_old = []

    if os.path.exists(target_check_json):
        try:
            with open(target_check_json, "r", encoding="utf-8") as jsonfile:
                old_data = json.load(jsonfile)
                package_old = [pkg.get("name") for pkg in old_data.get("packages", [])]
        except json.JSONDecodeError:
            pass

    package_new = []
    if os.path.exists(target_check_dir):
        for item in os.listdir(target_check_dir):
            item_path = os.path.join(target_check_dir, item)
            if os.path.isdir(item_path) and not item.startswith('.'):
                package_new.append(item)

    new_packages_list = []
        
    for pkg_folder in package_new:
        main_name = "main.py"
        main_location = os.path.join(target_path, pkg_folder, main_name)

        if os.path.exists(main_location):
            exec_name = f"rov{pkg_folder}" 
        else:
            continue

        req_location = os.path.join(target_path, pkg_folder)
        depends_required = check_depends(req_location)

        pkg_structure = {
            "name": pkg_folder,
            "executable": main_name,
            "cli": exec_name,
            "dependencies": depends_required
        }
        new_packages_list.append(pkg_structure)

    final_json_data = {"packages": new_packages_list}

    with open(target_check_json, "w", encoding="utf-8") as jsonwrite:
        json.dump(final_json_data, jsonwrite, indent=2, ensure_ascii=False)

    if not silent:
        print(f"[\033[94mINFO\033[0m] Found old packages: {package_old}")
        print(f"[\033[92mSUCCESS\033[0m] Updated package.json with: {package_new}")

def check_depends(pkg_folder_path):
    """
    Membaca requirements.txt di dalam folder package dan mengambil 
    nama-nama dependency-nya untuk dimasukkan ke dalam JSON.
    """
    req_file = os.path.join(pkg_folder_path, "requirements.txt")
    depends_required = {}

    if not os.path.exists(req_file):
        return depends_required

    try:
        with open(req_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Lewati baris kosong atau baris komentar (#)
                if not line or line.startswith("#"):
                    continue

                req_name = line
                req_version = "latest"  # Default jika tidak menulis versi khusus
                
                for char in ["==", ">=", "<=", ">", "<", "!="]:
                    if char in line:
                        parts = line.split(char)
                        req_name = parts[0].strip()
                        req_version = parts[1].strip() if len(parts) > 1 else "latest"
                        break

                depends_required[req_name] = req_version
                    
    except Exception as e:
        print(f"[\033[91mWARNING\033[0m] Gagal membaca {req_file}: {e}", file=sys.stderr)
        
    return depends_required