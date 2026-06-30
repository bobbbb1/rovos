#!/usr/bin/env python3
import os
import sys
import json
import subprocess
import time

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

def get_node_absolute_path(package, node_script, packages_cache):
    """Helper untuk mengambil path absolut dari suatu node script"""
    if package not in packages_cache:
        return None
    return os.path.normpath(os.path.join(packages_cache[package], package, node_script))

def launch_workspace(package, launch_file):
    """Membaca file *.launch.py dan mengeksekusi semua node di dalamnya secara simultan beserta konfigurasi YAML"""
    cache_file = os.path.join(WS_BUILD_PATH, "workspace_cache.json")
    if not os.path.exists(cache_file):
        print(f"[\033[91mERROR\033[0m] Build folder not found! Please rebuild.")
        return

    with open(cache_file, "r") as f:
        packages = json.load(f)

    if package not in packages:
        print(f"[\033[91mERROR\033[0m] Package '{package}' not found!")
        return

    launch_path = os.path.normpath(os.path.join(packages[package], "launch", launch_file))
    if not os.path.exists(launch_path):
        print(f"[\033[91mERROR\033[0m] Launch file not found in {launch_path}!")
        return

    print(f"[\033[94mLAUNCH\033[0m] Compiling Instruction from {launch_file}...")

    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("launch_mod", launch_path)
        launch_mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(launch_mod)
        launch_desc = launch_mod.generate_launch_description()
    except Exception as e:
        print(f"[\033[91mERROR\033[0m] Launch file execution failed: {e}")
        return

    nodes_to_run = launch_desc.get("nodes", [])
    if not nodes_to_run:
        print("[\033[93mWARN\033[0m] Cant find any nodes in this launch file.")
        return

    processes = []
    print(f"[\033[92mROVOS2\033[0m] Starting {len(nodes_to_run)} node...")
    print("-----------------------------------------------------------------------")

    try:
        for node_info in nodes_to_run:
            pkg_name = node_info.get("package")
            script_name = node_info.get("node")
            config_val = node_info.get("config", False)
            
            abs_path = get_node_absolute_path(pkg_name, script_name, packages)

            if abs_path and os.path.exists(abs_path):
                node_env = os.environ.copy()
                
                if config_val and config_val is not True:
                    config_path = os.path.normpath(os.path.join(packages[pkg_name], "config", config_val))
                    if os.path.exists(config_path):
                        node_env["ROVOS_CONFIG_PATH"] = config_path
                    else:
                        print(f"[\033[93mWARN\033[0m] File '{config_val}' not found in {config_path}!")
                
                proc = subprocess.Popen([sys.executable, abs_path], env=node_env)
                processes.append(proc)
                time.sleep(0.2)
            else:
                print(f"[\033[91mERROR\033[0m] Failed to launch node '{script_name}' (Path not found).")

        while True:
            alive_count = sum(1 for p in processes if p.poll() is None)
            if alive_count == 0:
                break
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\n[\033[93mLAUNCH\033[0m] Sending signal 'SIGINT' to process...")
    finally:
        for proc in processes:
            if proc.poll() is None:
                proc.terminate()
                proc.wait()
        print("[\033[92mSUCCESS\033[0m] Process has finished cleanly.")
